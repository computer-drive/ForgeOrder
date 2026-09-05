import pages from './pages.js'
import utils from './utils.js'


export function format(text, params = {}) {
    if (params) {
        text = text.replace(/\{([^{}]+)\}/g, (_, key) => {
            return key in params ? params[key] : `{${key}}`
        })
    }
    return text
}


export { pages, utils, format }

