import pagesRaw from './pages.jsonc?raw'
import componentsRaw from './components.jsonc?raw'
import utilsRaw from './utils.jsonc?raw'


import { parse } from 'jsonc-parser'

const pages = parse(pagesRaw)
const components = parse(componentsRaw)
const utils = parse(utilsRaw)

const cache = {}


export function t(key, params = {} ) {
    // 空key
    if (!key) {
        console.warn("无效的文案", key)
        return
    }
    
    let text = ''
    switch (key[0]) {
        case 'C':
            text = components
            key = key.slice(1)
            break
        case 'U':
            text = utils
            key = key.slice(1)
            break
        default:
            text = pages
            break
    }

    // 查找缓存
    if (cache[key]) {
        text = cache[key]
    } else {
    // 遍历查找
    for (let k of key.split('.')) {
            if (!text[k]) {
                console.warn("找不到文案：", key)
                return key
            }
            text = text[k]
        }

        // 若以$开头
        if (text[0] == '$') {
            return t(text.slice(1), params)
        }
        
        if (!text) {
            console.warn("找不到文案：", key)
            return key
        }

        // 缓存
        cache[key] = text
    }
    
    // 处理文案内部的引用参数
    const refParams = [...text.matchAll(/\{\$(.*?)\}/g)];

    for (const ref of refParams) {
        text = text.replace(ref[0], t(ref[1], params))
    }

    if (params) {
        text = text.replace(/\{([^{}]+)\}/g, (_, key) => {
            return key in params ? params[key] : `{${key}}`
        })
    }

    return text
}

export function locale(key, params= {}) {
    if (key && key[0] == '$') {
        return t(key.slice(1), params)
    } 
    return key
}