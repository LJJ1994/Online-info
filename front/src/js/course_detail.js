function CourseDetail() {

}

CourseDetail.prototype.run = function () {
   this.initPlayer();
};

CourseDetail.prototype.initPlayer = function () {
  var videoInfo = $('#video-info');
  var video_url = videoInfo.attr('data-video-url');
  var cover_url = videoInfo.attr('data-cover-url');
  var course_id = videoInfo.attr('data-course-id');

  var player = cyberplayer("playcontainer").setup({
      width: '100%',
      height: '100%',
      file: video_url,
      image: cover_url,
      autostart: false,
      stretching: "uniform",
      repeat: false,
      volume: 50,
      controls: true,
      tokenEncrypt: true,
      // 这里的ak是百度云的AccessKey,在安全认证/accesskey
      ak: '72d3fdc507ba4dadbf33b8193138327d'
  });
  player.on('beforePlay', function (e) {
      if(!/m3u8/.test(e.file)){ //如果视频部署m3u8格式，直接返回
         return;
      }

      $.get({
         url: '/course/course_token/',
         data: {
            'video': video_url,
            'course_id': course_id
         },
         success: function (res) {
            if (res.code===200) {
               var token = res['data']['token'];
               player.setToken(e.file, token);
            } else {
               window.messageBox.showError(res.message);
               player.stop();
            }
         },
         error: function (res) {
            console.log(res);
         }
      })
  })
};

$(function () {
   var courseDetail = new CourseDetail();
   courseDetail.run();
});