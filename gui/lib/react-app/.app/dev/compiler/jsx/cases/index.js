const cases = {
    css: require('./css'),
    svg: require('./svg')
}



module.exports = ($, url, type, currentUrl) => {
    //console.log(url,currentUrl);
    return cases[type] ? cases[type]($, url, currentUrl) : `${$} "${url}"`;
};