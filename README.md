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
