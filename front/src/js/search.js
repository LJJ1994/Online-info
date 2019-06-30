function  NewsSearch() {

}

NewsSearch.prototype.run = function () {
   var searchBtn = $('.search-btn');
   var hasQuery = $('.search-input').val();

   // if (!hasQuery) {
   //    $.get({
   //       url: '/news/search/',
   //       success: function (res) {
   //          console.log(res);
   //       }
   //    })
   // }
   // searchBtn.click(function (e) {
   //    e.preventDefault();
   //
   // })
};

$(function () {
   var newsSearch = new NewsSearch();
   newsSearch.run();
});
