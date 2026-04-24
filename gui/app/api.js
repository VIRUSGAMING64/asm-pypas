

class API{
    constructor(){
        this.base = "/api/"
    }

    async fetchapi(url){
        var res=await fetch(this.base + url)
        var json = await res.json()
        return json
    }
    async getcode(name){
        var data = await this.fetchapi("getcode?name="+name)
        console.log(data)
        return data["code"]
    }
    async initcodes(){
        return this.fetchapi("initcodes")
    }
    async newcode(name){
        return this.fetchapi("newcode?name=" + encodeURIComponent(name))
    }
    async delcode(name){
        return this.fetchapi("delcurr?name=" + encodeURIComponent(name))
    }
    async save(name, code){
        const payload = {
            name,
            code
        }

        let response = await fetch("/api/save", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        })
        return await response.json()
    }
    async run(name, code){
        
        const payload = {
            name,
            code
        }

        let response = await fetch("/api/run", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        })
        return await response.json()

    }

};


export default API