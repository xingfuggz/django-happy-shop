/**
 * gulp API说明
 * 文档：https://www.gulpjs.com.cn/docs/api/concepts/
 * series()    组合任务函数，按顺序执行
 * parallel()  组合任务函数，最大并发执行
 * src()       创建一个流，读取文件
 * dest()      移动文件到指定目录
 * watch()     监听文件任务
 */
 const { series, src, dest, watch, parallel } = require('gulp');

 // browserSync文档： http://www.browsersync.cn/docs/gulp/
 const browserSync = require('browser-sync').create()    // 自动刷新浏览器
 const reload      = browserSync.reload;
 
 /**
  * 插件说明
  * 安装：npm install --save-dev 插件名称
  * 编译sass需要额外全局安装 npm install -g sass
  */
 const rename = require('gulp-rename');   // 修改名字
 const concat = require('gulp-concat');   // 合并多个文件到一个文件
 const uglify = require('gulp-uglify');   // 压缩js文件
 const csso   = require('gulp-csso');     // 压缩css文件
 const sass   = require('gulp-sass')(require('sass'));    // 编译sass


// 迁移product html
function ProductHtml() {
  return src('templates/*/*.html')
  .pipe(dest('../templates/'))
  // .pipe(dest(dist_html.dadmin))
  .pipe(browserSync.reload({stream:true}))
};

// 迁移Base html
function BaseHtml() {
  return src('templates/*.html')
  .pipe(dest('../templates/'))
  // .pipe(dest(dist_html.dadmin))
  .pipe(browserSync.reload({stream:true}))
};

 
 // sass编译为css,并迁移到src/css文件夹
 function buildStyles() {
     return src('static/*/css/*.scss')
       .pipe(sass().on('error', sass.logError))
       .pipe(csso())
       .pipe(rename({suffix: "-min"}))
       .pipe(dest('../static/'))
       .pipe(browserSync.reload({stream:true}))
   };
  
 // sass编译为css,并迁移到src/css文件夹
 function ScssNextCss() {
  return src('static/*/css/*.scss')
    .pipe(sass().on('error', sass.logError))
    // .pipe(csso())
    // .pipe(rename({suffix: "-min"}))
    .pipe(dest('../static/'))
    .pipe(browserSync.reload({stream:true}))
};
 
 // 迁移src/css文件压缩改名到dist/css目录
//  function css() {
//    return src('src/css/*.css')
//    .pipe(dest('dist/css/'))
//    .pipe(browserSync.reload({stream:true}))
//  };
 
 // 迁移src/js文件压缩改名到dist/js目录
 function ProductScript() {
   return src('static/*/js/*.js')
  //  .pipe(rename({suffix: ".min"}))
   .pipe(dest('../static/'))
   .pipe(browserSync.reload({stream:true}))
 };
 
 // 监听
 function watchr() {
   watch('templates/*.html', BaseHtml);
   watch('templates/*/*.html', ProductHtml);
   watch('static/*/css/*.scss', ScssNextCss);
   watch('static/*/js/*.js', ProductScript);
 };
 
 // 静态服务器
 function serve() {
   browserSync.init({
     server: {
       baseDir: "dist/"
     }
   });
   watchr();
 };


 // 代理
 function ServeSync() {
  browserSync.init({
    proxy: "127.0.0.1:8000"
  });
  watchr();
 }

 exports.ProductHtml = ProductHtml;     // 迁移html
 exports.BaseHtml = BaseHtml;           // 迁移html
 exports.ScssNextCss = ScssNextCss;     // 编译并迁移scss文件
 exports.ProductScript = ProductScript; // 迁移JS文件
 exports.build = parallel(ProductHtml, ScssNextCss, ProductScript);
 exports.default =  ServeSync;
 