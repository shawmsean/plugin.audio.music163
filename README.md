# 网易云音乐 Kodi 插件

### 下载

到 [Actions](https://github.com/chen310/plugin.audio.music163/actions)（推荐） 或 [Releases](https://github.com/chen310/plugin.audio.music163/releases)（更新不及时） 中下载

### 截图

![主页](https://cdn.jsdelivr.net/gh/chen310/plugin.audio.music163/public/home.png)
![歌单](https://cdn.jsdelivr.net/gh/chen310/plugin.audio.music163/public/playlist.png)
![播放歌曲](https://cdn.jsdelivr.net/gh/chen310/plugin.audio.music163/public/song.png)
![播放MV](https://cdn.jsdelivr.net/gh/chen310/plugin.audio.music163/public/mv.png)
![设置](https://cdn.jsdelivr.net/gh/chen310/plugin.audio.music163/public/settings.png)

### 更新日志

#### 2025-12-23

1. **修复每日推荐在Kodi小部件中的连续播放功能**：
   - 新增`play_recommend_songs()`函数，专门处理每日推荐歌曲的播放列表构建和播放
   - 修改`get_songs_items()`函数，当`source='recommend_songs'`时，将歌曲的播放路径指向新的播放函数
   - 确保播放列表包含所有可播放的歌曲，并从选中的歌曲开始播放
   - 修复媒体信息显示问题，确保第一首歌曲能正确显示歌名等信息

2. **扩展所有歌单的连续播放功能**：
   - 新增`play_playlist_songs()`函数，通用处理任何歌单类型的连续播放
   - 修改`get_songs_items()`函数，当`source='playlist'`时，将歌曲的播放路径指向新的播放函数
   - 修改`playlist()`函数，传递`source='playlist'`参数以正确识别歌单类型
   - 现在所有歌单（包括用户歌单、热门歌单、推荐歌单等）在小部件中都能连续播放

3. **修复存储相关错误**：
   - 修复`safe_get_storage()`函数，确保总是返回包含所需键的默认字典
   - 处理存储文件不存在的情况，避免KeyError异常
   - 确保不同存储类型（liked_songs、account、time_machine等）都有适当的默认结构

4. **改进播放体验**：
   - 修复播放列表构建逻辑，确保所有可播放歌曲都被包含
   - 处理超过1000首歌的歌单情况
   - 确保媒体信息正确显示，包括歌名、艺术家、专辑等
   - 添加错误处理，当播放列表为空时显示友好的错误提示

这些修改使得插件在Kodi小部件中的播放体验更加流畅，特别是在Embuary皮肤中使用时，能够实现连续播放整个歌单或每日推荐列表，而不仅仅是单首歌曲。

#### 2025-12-28
1. **集成GD音乐台作为备用解析源**：
   - 添加了GD音乐台解析服务（`gdmusic.py`）作为备用音乐解析源
   - 新增`get_song_url_with_gdmusic_fallback()`辅助函数，实现智能备用解析逻辑
   - 修改了所有关键播放函数（`song_contextmenu()`、`play()`、`play_recommend_songs()`、`play_playlist_songs()`）以使用新的备用解析机制
   - 当网易云音乐原有API无法获取播放链接时，系统会自动尝试使用GD音乐台解析
   - 添加了完整的错误处理和日志记录功能
   - 保持了向后兼容性，所有原有功能不受影响

2. **提升歌曲可播放性**：
   - 显著提高了在网易云音乐API限制或不可用情况下的歌曲可播放性
   - 支持多个备用音源（Joox、Tidal、Netease）通过GD音乐台解析
   - 自动尝试不同音源以提高解析成功率
   - 优雅处理解析失败情况，不影响用户体验

3. **技术改进**：
   - 所有修改遵循原有代码风格和规范
   - 添加了详细的函数文档和注释
   - 保持了代码的可读性和可维护性
   - 所有修改经过仔细测试和验证

这个集成工作使得插件在面对网易云音乐API限制时，能够提供更稳定和可靠的播放体验，特别是对于受版权限制或地域限制的歌曲。
