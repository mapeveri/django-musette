const gulp = require('gulp');		
const concat = require('gulp-concat');		
const minifyCSS = require('gulp-minify-css');		
	
gulp.task('minified-css', function() {		
  return gulp.src('musette/static/musette/css/*.css')		
    .pipe(minifyCSS())		
    .pipe(concat('style.min.css'))		
    .pipe(gulp.dest('musette/static/musette/css'))		
});