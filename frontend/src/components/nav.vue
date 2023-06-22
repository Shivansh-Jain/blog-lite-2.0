<template>
    <nav class="navbar navbar-expand-lg bg-body-secondary" data-bs-theme="dark">
    <div class="container-fluid">
        <RouterLink to="/profile">
        <a class="navbar-brand">
            <div class="d-flex align-items-center mx-2">
                <img :src="require(`@/assets/profile/${user_id}.jpg`)" style="border-radius: 50%;" width="40"
                    height="40" class="d-inline-block" :title="username">
                
            </div>
        </a>
    </RouterLink>
      <button class="navbar-toggler collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#navbarColor01" aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="navbar-collapse collapse" id="navbarColor01" style="">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink to="/newsfeed" style="text-decoration: none;">
                <a class="nav-link" type="button" style="border: 0;" >
                        Home
                </a>
                </RouterLink>
          </li>
          <li class="">
            <a class="nav-link" type="button" style="border: 0;" data-bs-toggle="modal" data-bs-target="#exampleModal">
                        Create Post
            </a>
                    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel"
                        aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h1 class="modal-title fs-5" id="exampleModalLabel">Modal title</h1>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                                        aria-label="Close"></button>
                                </div>

                                <form @submit.prevent="create" style="max-width: 50%;padding-top: 5%;" class="m-auto"
                                    enctype="multipart/form-data">
                                    <div class="modal-body">
                                        <!-- <img class="mb-4" src="/docs/5.2/assets/brand/bootstrap-logo.svg" alt="" width="72" height="57"> -->
                                        <h1 class="h3 mb-3 fw-normal" style="color: white;">Create Post</h1>

                                        <div class="form-floating pt-1">
                                            <div class="form-control pt-0 pb-5">
                                                <p style="margin-bottom: 0.2cm;">Select an Image</p>
                                                <input @change="handle_image" ref="pimage" name="pimage" type="file"
                                                    accept="image/jpeg,image/png">
                                            </div>
                                        </div>
                                        <div class="form-floating">
                                            <input class="form-control"  v-model="title" name="title" placeholder="Title"
                                                required>
                                            <label for="floatingtitle">Title</label>
                                        </div>
                                        <div class="form-floating">
                                            <input v-model="caption"  class="form-control" name="caption"
                                                placeholder="write your caption here">
                                            <label for="floatingcaption">Caption</label>
                                        </div>
                                        <div class="modal-footer">
                                            <button class="w-100 btn btn-lg btn-primary" type="submit">Post</button>

                                        </div>
                                    </div>
                                </form>


                            </div>
                        </div>
                    </div>
          </li>
          <li class="nav-item">
            <a class="nav-link" @click="export_pdf">Export</a>
          </li>
        </ul>
        <div class="d-flex" role="search">
          <input v-model="entry" class="form-control my-2" type="search" placeholder="Search" aria-label="Search">
          <button type="submit" class="btn btn-outline-light my-2"  @click="search" id="basic-addon1" data-bs-toggle="modal"
                                data-bs-target="#search">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
              <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"></path>
            </svg></button>
            <div class="modal fade" id="search" tabindex="-1" aria-labelledby="exampleModalLabel"
                                aria-hidden="true">
                                <div class="modal-dialog">
                                    <div class="modal-content">
                                        <div class="modal-header">
                                            <h1 class="modal-title fs-5" id="exampleModalLabel">Search Results</h1>
                                            <button type="button" @click="reload" class="btn-close" data-bs-dismiss="modal"
                                                aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                            <div class="container">
                                                <div v-for="acc in accounts" v-bind:key="acc.user_id">
                                                    <div class="row">
                                                        <div class="col-sm-1">
                                                            <img :src="require(`@/assets/profile/${acc.user_id}.jpg`)"
                                                                style="border-radius: 50%;" width="40" height="40"
                                                                class="d-inline-block align-top" alt="">
                                                        </div>
                                                        <div class="col-sm-4">
                                                            <RouterLink :to="'/other/'+acc.user_id" >
                                                            <p data-bs-dismiss="modal">{{ acc.name }}</p></RouterLink>
                                                        </div>
                                                        <div class="col-sm-7">
                                                            <div v-if="following.includes(acc.user_id)">
                                                            <button type="button" class="btn btn-light" @click="unfollow(acc.user_id)" style="float: right;">Unfollow</button>
                                                            </div>
                                                            <div v-else>
                                                            <button type="button" class="btn btn-primary" @click="follow(acc.user_id)" style="float: right;">Follow</button>
                                                            </div>

                                                    </div>
                                                    </div><br>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
        
        </div>
        <button class="btn btn-outline-light m-2" @click="logout">Logout</button>

      </div>
    </div>
  </nav>
</template>

<script>
import router from '@/router'



export default {
    name: "NavBar",
    data() {
        return {
            find: false,
            accounts: null,
            entry: "",
            user_id: localStorage.getItem("user_id"),
            username: localStorage.getItem('username'),
            following:[],
            cpost: false,
            title: '',
            caption: '',
            image: null,
 
        }
    },
    computed:{
        image_path(){
            return "/img/"+localStorage.getItem('user_id')+'.jpg'
        }
    },
    mounted(){
        fetch("http://127.0.0.1:8000/api/follow/"+localStorage.getItem('user_id')+'/False',{
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem("access_token")
                },
                method: "GET",
            })
            .then((response)=>{
                return response.json()
            })
            .then((data)=>{
                // console.log(data.accounts[0]['following'])
                const temp=data.accounts;
                temp.forEach(element => {
                    console.log(element['following'])
                    this.following.push(element['following'])
                });
            })
    },
    methods: {
        export_pdf(){
            fetch("http://127.0.0.1:8000/csv/"+localStorage.getItem('user_id'),{
                headers:{
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin":"*",
                    Authorization:"Bearer "+localStorage.getItem('access_token')
                },
                method:"GET"
            })
            .then((response)=>{
                if(response){
                    alert("Your report has been Generated")
                }
            })
        },


        reload(){
            window.location.reload()
        },
        follow(id){
            fetch("http://127.0.0.1:8000/api/follow",{
                headers:{
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin":"*",
                    Authorization:"Bearer "+localStorage.getItem('access_token')
                },
                method:"POST",
                body: JSON.stringify({
                    following:id
                }),
            })
           .then((response)=>{
                if(response.ok){
                    
                    this.following.push(id)
                    // window.location.reload()
                
                }
                console.log(response)
                return response.json()
           })

        },
        unfollow(id){
            fetch("http://127.0.0.1:8000/api/follow",{
                headers:{
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin":"*",
                    Authorization:"Bearer "+localStorage.getItem('access_token')
                },
                method:"DELETE",
                body: JSON.stringify({
                    following:id
                }),
            })
           .then((response)=>{
                if(response.ok){
                   
                    this.following=this.following.filter(x => x != id)
                }
                console.log(response)
                return response.json()
           })

        },
        logout() {
            localStorage.removeItem('user_id')
            localStorage.removeItem('access_token')
            localStorage.removeItem('username')
            router.push('/')
        },


        post() {
            this.cpost = true
        },
        handle_image() {
            this.image = this.$refs.pimage.files[0];
        },
        create() {
            const formData = new FormData;
            formData.append('image', this.image)
            formData.append('title', this.title)
            formData.append('caption', this.caption)
            fetch("http://127.0.0.1:8000/api/posts", {
                method: "POST",
                headers: {
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem("access_token")
                },
                body: formData

            })
                .then((response) => {
                    if (response.ok) {
                        console.log("post created");
                        alert("post created");
                    }
                })
                .catch((err) => {
                    console.log(err);
                })
        },



        search() {
            this.find = true;
            fetch("http://127.0.0.1:8000/api/accounts/" + this.entry + '/True/' + 'False', {
                method: "GET",
            })
            .then((response) => {
                    if (!response.ok) {
                        console.log('some error')
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.status) {
                        this.accounts = data.accounts
                        console.log(this.accounts);

                    }
                })
                .catch((err) => {
                    console.log(err);
                })

        }
    }

}

</script>
