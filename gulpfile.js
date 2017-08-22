const path = require('path');
const gulp = require('gulp');		
const concat = require('gulp-concat');		
const minifyCSS = require('gulp-minify-css');	
const webpack = require('webpack');	
const gulpWebpack = require('webpack-stream');

//Compile and minified js
gulp.task('js', function() {
  return gulp.src('')
    .pipe(gulpWebpack({
      watch: true,
      entry: {
          'index': "./musette/static/musette/js/modules/musette/index.js",
      },
      output: {
          path: path.resolve('./musette/static/musette/js/modules/'), 
          filename: "musette.module.min.js"
      },
      
      plugins: [
          /**
           * See description in 'webpack.config.dev' for more info.
           */
          new webpack.DefinePlugin({
              'process.env.NODE_ENV': JSON.stringify('production')
          }),
          /**
           * Some of you might recognize this! It minimizes all your JS output of chunks.
           * Loaders are switched into a minmizing mode. Obviously, you'd only want to run
           * your production code through this!
           */
          new webpack.optimize.UglifyJsPlugin({
              compressor: {
                  warnings: false
              }
          }),
          //Initial jquery
          new webpack.ProvidePlugin({
              $: "jquery",
              jquery: "jquery",
              "windows.jQuery": "jquery",
              jQuery:"jquery",
          })
      ],

      externals: {
          // Use external version of React and react-dom
          "jquery": "jQuery",
      },

      module: {
          loaders: [
              //a regexp that tells webpack use the following loaders on all 
              //.js and .jsx files
              {
                  test: /\.jsx?$/, 
                  //we definitely don't want babel to transpile all the files in 
                  //node_modules. That would take a long time.
                  exclude: /node_modules/, 
                  //use the babel loader 
                  loader: 'babel-loader', 
                  query: {
                      //specify that we will be dealing with
                      presets: ['es2015', 'es2016']
                  }
              }
          ]
      }
    }))
    .pipe(gulp.dest('musette/static/musette/js/modules'));
});

//Minified css files
gulp.task('css', function() {		
  return gulp.src('musette/static/musette/css/*.css')		
    .pipe(minifyCSS())		
    .pipe(concat('style.min.css'))		
    .pipe(gulp.dest('musette/static/musette/css'))		
});
