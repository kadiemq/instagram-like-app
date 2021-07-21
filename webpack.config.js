const path = require('path')

module.exports = {
    mode: 'development',
    entry: "./index.js",
    output: {
        filename: 'index_bundle.js',
        path: path.resolve(__dirname, 'static')
    },
    module: {
        rules: [{
            test: /\.js$/,
            exclude: /node_modules/,
            use: {loader: "babel-loader"}
        }, {
            test: /\.css$/,
            use: ["style-loader", "css-loader"]
        }]
    }
}