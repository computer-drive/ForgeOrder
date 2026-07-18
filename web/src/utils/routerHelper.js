import router from "@/router.js"

const fromPages = []

export function pushWithFrom(target, extraQuery = {}) {
    
    let routeConfig = typeof target === 'string' 
        ? { path: target } 
        : { ...target }

    const currentPath = router.currentRoute.value.fullPath

    fromPages.push({
        path: routeConfig.path,
        from: currentPath,
    })
    

    const query = {
        ...routeConfig.query,
        ...extraQuery
    }

    console.log(fromPages)

    return router.push({
        path: routeConfig.path,
        query: query,
        ...(routeConfig.name && { name: routeConfig.name }),
        ...(routeConfig.params && { params: routeConfig.params }),
    })
}

export function goBack() {
    // console.log(fromPages)
    const currentPath = router.currentRoute.value.path
    
    const fromPath = fromPages.find(item => item.path === currentPath)

    if (fromPath) {

        router.push(fromPath.from, { transition: 'tabslide-left' })

        fromPages.splice(fromPages.indexOf(fromPath), 1)

    } else {
        // console.log(1)
        // 返回到上一级
        const backPath = currentPath.split('/').slice(0, -1).join('/') || '/'
        
        
        router.push(backPath)
    }
}


