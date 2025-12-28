#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GD音乐台解析服务 - Python版本
基于原TypeScript代码转换而来
"""

import asyncio
import json
from typing import Dict, Any, Optional, List, Union
import requests
from urllib.parse import quote

# 定义数据结构
class GDMusicResponse:
    """GD音乐解析结果数据结构"""
    def __init__(self, url: str, br: int, size: int, md5: str, platform: str, gain: int):
        self.url = url
        self.br = br
        self.size = size
        self.md5 = md5
        self.platform = platform
        self.gain = gain

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'url': self.url,
            'br': self.br,
            'size': self.size,
            'md5': self.md5,
            'platform': self.platform,
            'gain': self.gain
        }

class ParsedMusicResult:
    """最终解析结果格式"""
    def __init__(self, data: Dict[str, Any], params: Dict[str, Any]):
        self.data = data
        self.params = params

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'data': self.data,
            'params': self.params
        }

class GDMusicUrlResult:
    """音乐URL结果"""
    def __init__(self, url: str, br: str, size: int, source: str):
        self.url = url
        self.br = br
        self.size = size
        self.source = source

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'url': self.url,
            'br': self.br,
            'size': self.size,
            'source': self.source
        }

# 可用音乐源
ALL_SOURCES = ['joox', 'tidal', 'netease']
BASE_URL = 'https://music-api.gdstudio.xyz/api.php'

async def parse_from_gd_music(
    id: int,
    data: Dict[str, Any],
    quality: str = '999',
    timeout: int = 15000
) -> Optional[Dict[str, Any]]:
    """
    从GD音乐台解析音乐URL

    Args:
        id: 音乐ID
        data: 音乐数据，包含名称和艺术家信息
        quality: 音质设置，默认'999'表示最高音质
        timeout: 超时时间(毫秒)，默认15000ms

    Returns:
        解析后的音乐URL及相关信息，或None表示解析失败
    """
    try:
        # 使用asyncio.wait_for实现超时控制
        result = await asyncio.wait_for(
            _parse_from_gd_music_inner(id, data, quality),
            timeout=timeout/1000  # 转换为秒
        )
        return result
    except asyncio.TimeoutError:
        print('GD音乐台解析超时')
        return None
    except Exception as e:
        print(f'GD音乐台解析完全失败: {str(e)}')
        return None

async def _parse_from_gd_music_inner(
    id: int,
    data: Dict[str, Any],
    quality: str = '999'
) -> Optional[Dict[str, Any]]:
    """
    内部解析函数
    """
    # 处理不同数据结构
    if not data:
        print('GD音乐台解析：歌曲数据为空')
        raise ValueError('歌曲数据为空')

    # 提取歌曲名称
    song_name = data.get('name', '')

    # 提取艺术家名称
    artist_names = ''
    if 'artists' in data and isinstance(data['artists'], list):
        artist_names = ' '.join([artist.get('name', '') for artist in data['artists']])
    elif 'ar' in data and isinstance(data['ar'], list):
        artist_names = ' '.join([artist.get('name', '') for artist in data['ar']])
    elif 'artist' in data:
        artist_names = data['artist'] if isinstance(data['artist'], str) else ''

    search_query = f"{song_name} {artist_names}".strip()

    if not search_query or len(search_query) < 2:
        print('GD音乐台解析：搜索查询过短', {'name': song_name, 'artists': artist_names})
        raise ValueError('搜索查询过短')

    print('GD音乐台开始搜索:', search_query)

    # 依次尝试所有音源
    for source in ALL_SOURCES:
        try:
            result = await search_and_get_url(source, search_query, quality)
            if result:
                print(f'GD音乐台成功通过 {result.source} 解析音乐!')
                # 返回符合原API格式的数据
                return {
                    'data': {
                        'data': {
                            'url': result.url.replace('\\', ''),
                            'br': int(result.br) * 1000 if result.br else 320000,
                            'size': result.size or 0,
                            'md5': '',
                            'platform': 'gdmusic',
                            'gain': 0
                        },
                        'params': {
                            'id': int(id),
                            'type': 'song'
                        }
                    }
                }
        except Exception as e:
            print(f'GD音乐台 {source} 音源解析失败: {str(e)}')
            # 该音源失败，继续尝试下一个音源
            continue

    print('GD音乐台所有音源均解析失败')
    return None

async def search_and_get_url(
    source: str,
    search_query: str,
    quality: str
) -> Optional[GDMusicUrlResult]:
    """
    在指定音源搜索歌曲并获取URL

    Args:
        source: 音源
        search_query: 搜索关键词
        quality: 音质

    Returns:
        音乐URL结果或None
    """
    # 1. 搜索歌曲
    search_url = f"{BASE_URL}?types=search&source={source}&name={quote(search_query)}&count=1&pages=1"
    print(f'GD音乐台尝试音源 {source} 搜索: {search_url}')

    try:
        search_response = requests.get(search_url, timeout=5)
        search_data = search_response.json()

        if search_data and isinstance(search_data, list) and len(search_data) > 0:
            first_result = search_data[0]
            if not first_result or 'id' not in first_result:
                print(f'GD音乐台 {source} 搜索结果无效')
                return None

            track_id = first_result['id']
            track_source = first_result.get('source', source)

            # 2. 获取歌曲URL
            song_url = f"{BASE_URL}?types=url&source={track_source}&id={track_id}&br={quality}"
            print(f'GD音乐台尝试获取 {track_source} 歌曲URL: {song_url}')

            song_response = requests.get(song_url, timeout=5)
            song_data = song_response.json()

            if song_data and 'url' in song_data:
                return GDMusicUrlResult(
                    url=song_data['url'],
                    br=song_data.get('br', '320'),
                    size=song_data.get('size', 0),
                    source=track_source
                )
            else:
                print(f'GD音乐台 {track_source} 未返回有效URL')
                return None
        else:
            print(f'GD音乐台 {source} 搜索结果为空')
            return None
    except Exception as e:
        print(f'GD音乐台 {source} 请求失败: {str(e)}')
        return None

# 同步封装函数，便于直接调用
def parse_from_gd_music_sync(
    id: int,
    data: Dict[str, Any],
    quality: str = '999',
    timeout: int = 15000
) -> Optional[Dict[str, Any]]:
    """
    同步版本的GD音乐台解析函数

    Args:
        id: 音乐ID
        data: 音乐数据
        quality: 音质设置
        timeout: 超时时间

    Returns:
        解析结果或None
    """
    # 创建事件循环并运行异步函数
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(
            parse_from_gd_music(id, data, quality, timeout)
        )
        return result
    finally:
        loop.close()

if __name__ == '__main__':
    # 示例用法
    example_data = {
        'name': '爱',
        'artists': [{'name': '小虎队'}]
    }

    print('开始测试GD音乐台解析...')
    result = parse_from_gd_music_sync(456856931, example_data)
    if result:
        print('解析成功!')
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print('解析失败!')
