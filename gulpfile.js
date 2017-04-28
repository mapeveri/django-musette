const gulp = require('gulp');
const concat = require('gulp-concat');
const uglify = require('gulp-uglify');
const minifyCSS = require('gulp-minify-css');

gulp.task('minified-js', function() {
  var src = [
      'musette/static/musette/js/modules/musette.module.js',
  ];

  return gulp.src(src)
    .pipe(concat('musette.module.min.js'))
    .pipe(uglify())
    .pipe(gulp.dest('musette/static/musette/js/modules'))
});

gulp.task('minified-css', function() {
  return gulp.src('musette/static/musette/css/*.css')
    .pipe(minifyCSS())
    .pipe(concat('style.min.css'))
    .pipe(gulp.dest('musette/static/musette/css'))
});
