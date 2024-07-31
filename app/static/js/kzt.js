
var liItem = document.getElementsByClassName("li_item");
var liSelect = document.getElementsByClassName("li_select")[0];
var articleContent = document.getElementsByClassName('article_content')
// 循环找到被点击的下角标
// 提前预加载的 文章的内容
articleContent[0].classList.add('article_content_none');
liItem[0].classList.add('c_li');
liSelect.addEventListener('click',function (event){
    // 确保点击的是子元素
    var target = event.target;
    // js 代码中的 this 有可能指的是整个 windows 整个页面的内容
    while (target && target !== this){
        if (target.tagName.toLowerCase() === 'li'){
            // 获取li的索引位置
            var index = Array.from(this.children).indexOf(target);
            console.log("索引的位置是",index);
            // 这边是获取不到下角标
            articleContent[index].classList.add('article_content_none');
            break;

        }
    }
})
// 清除所有的样式
    document.querySelectorAll('.li_item').forEach(function(l1) {
  l1.addEventListener('click', function() {
    // 移除所有 li 的 c_li 类
    document.querySelectorAll('.li_item').forEach(function(li) {
      li.classList.remove('c_li');

    });
    document.querySelectorAll('.article_content').forEach(function (div){
        div.classList.remove('article_content_none');
        articleContent[0].classList.remove('article_content_none');

    })
         l1.classList.add('c_li');
       });


})


