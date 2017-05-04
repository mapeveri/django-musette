//require our dependencies
const path = require('path')
const webpack = require('webpack')
const BundleTracker = require('webpack-bundle-tracker')

module.exports = {
    //the base directory (absolute path) for resolving the entry option
    context: __dirname,
    //the entry point we created earlier. Note that './' means 
    //your current directory. You don't have to specify the extension  now,
    //because you will specify extensions later in the `resolve` section
    entry: {
        'index': "./musette/static/musette/js/modules/musette/index.js",
    },
    output: {
        path: path.resolve('./musette/static/musette/js/modules/'), 
        filename: "musette.module.min.js"
    },
    
    plugins: [
        //tells webpack where to store data about your bundles.
        new BundleTracker({filename: './webpack-stats.json'}), 
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
}