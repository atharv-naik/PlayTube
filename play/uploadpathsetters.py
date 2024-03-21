import os

def getVideoUploadPath(instance, filename):
    # returns ex. videos/channel_id/video_id/title.mp4
    return os.path.join('videos', f"{instance.channel.channel_id}", f"{instance.video_id}", f"{instance.title}.{filename.split('.')[-1]}")

def getSubtitleUploadPath(instance, filename):
    # returns ex. videos/channel_id/video_id/subtitles/subtitle.srt
    return os.path.join('videos', f"{instance.channel.channel_id}", f"{instance.video_id}", "subtitles", f"subtitle.{filename.split('.')[-1]}")

def getThumbnailUploadPath(instance, filename):
    # returns ex. videos/channel_id/video_id/thumbnails/thumbnail.jpg
    return os.path.join('videos', f"{instance.channel.channel_id}", f"{instance.video_id}", "thumbnails", f"thumbnail.{filename.split('.')[-1]}")

def getChannelAvatarUploadPath(instance, filename):
    # returns ex. avatars/channel_id/avatar.jpg
    return os.path.join('avatars', f"{instance.channel_id}", f"avatar.{filename.split('.')[-1]}")

def getChannelBannerUploadPath(instance, filename):
    # returns ex. banners/channel_id/banner.jpg
    return os.path.join('banners', f"{instance.channel_id}", f"banner.{filename.split('.')[-1]}")