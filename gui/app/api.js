

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
        this.fetchapi("initcodes/")
    }
    async newcode(){
        this.fetchapi("newcode/")
    }
    async delcode(){
        this.fetchapi("delcode/")
    }
    async save(){
        this.fetchapi("save/")
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