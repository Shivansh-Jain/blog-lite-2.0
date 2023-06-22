<template>
    <NavBar></NavBar>
    <!-- <p>{{posts}}</p> -->
    <div v-for="(post,index) in posts" v-bind:key="post.post_id">
        <div v-if="following.includes(post.user_id)">
            <div class="card m-auto mb-3 sdw" style="">
                <!-- <div class="card-header">{{ post.profile }}</div> -->
                <div class="row g-0 " >
                    <div data-bs-toggle="modal" :data-bs-target="modalTarget(post.post_id)"
                    @click="loadComment(post.post_id)">
                    <div >
                        <img class="img-fluid" :src="require(`@/assets/posts/${post.post}`)" alt="Image" />
                    </div>
                    <div class="col-md-4">
                        <div class="card-body">
                            <h4 class="card-title" style="text-align: left;" :v-html="post.title">{{ post.title }}</h4>
                            <p class="card-text"
                                style="text-align: left;max-height: 2cm;overflow: hidden;margin-bottom: 1cm;" :v-html="post.caption">{{
                                    post.caption }}</p>
                        </div></div></div>
                        <div class="card-footer">
                            <div class="row g-0">
                                <div class="col-md-1">
                                    <img class="img-fluid" :src="require(`@/assets/profile/${post.user_id}.jpg`)"
                                        style="height: 40px;width: 40px;border-radius: 20px;background-color: grey;" />
                                </div>
                                <div class="col-md-4" style="text-align: left;">
                                    <RouterLink :to="'/other/'+post.user_id">
                                    <h5>{{ post.name }}</h5></RouterLink>
                                </div>
                                <div class="col" style="text-align: right;">
                                    <p class="card-text"><small class="text-body-secondary">{{ post.timestamp }}
                                        </small></p>
                                </div>
                            </div>

                        </div>
                    
                </div>
                <div class="modal fade" :id="Id(post.post_id)" tabindex="-1" aria-labelledby="pageLabel" aria-hidden="true">
                    <div class="modal-dialog  modal-xl">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h1 class="modal-title fs-5" id="pageLabel">{{ post.title }}</h1>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="model-body">
                                <div class="container-fluid">
                                    <div class="row d-flex">
                                        <div class=" col-md-4">
                                            <img :src="require(`@/assets/posts/${post.post}`)"
                                                class="img-fluid rounded-start" alt="...">
                                        </div>
                                        <div class="col-md-8">
                                            <div class="">
                                                <!-- <h5 class="card-title">Card title</h5> -->
                                                <p class="">{{ post.caption }}</p>

                                            </div>
                                        </div>
                                    </div><br>
                                    <div class="row d-flex">
                                        <div class="col-xxl">
                                            <div class="">
                                                <div class="">
                                                    <h5>Comments</h5>
                                                </div>
                                                <div class="">
                                                    <div class="container">
                                                        <div v-for="com in comments" v-bind:key="com.comment_id">
                                                            <div class="row p-0">
                                                                <div class="col-sm-1">
                                                                    <img class="img-fluid"
                                                                        :src="require(`@/assets/profile/${com.user_id}.jpg`)"
                                                                        style="height: 40px;width: 40px;border-radius: 20px;background-color: grey;" />
                                                                </div>
                                                                <div class="col-sm-2" style="float: left;text-align: left;">
                                                                    <h4>{{ com.name }}</h4>
                                                                </div>
                                                                <div class="col-md-5" style="text-align: left;">{{
                                                                    com.comment
                                                                }}</div>
                                                            </div>
                                                            <br>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <div class="row">
                                    <div class="card-footer">
                                        <div v-if="post.liked_by.includes(user_id)">
                                        <button @click="unlike(post.post_id,index)" type="button" class="btn btn-secondary">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                fill="currentColor" class="bi bi-suit-heart-fill" viewBox="0 0 16 16">
                                                <path
                                                    d="M4 1c2.21 0 4 1.755 4 3.92C8 2.755 9.79 1 12 1s4 1.755 4 3.92c0 3.263-3.234 4.414-7.608 9.608a.513.513 0 0 1-.784 0C3.234 9.334 0 8.183 0 4.92 0 2.755 1.79 1 4 1z" />
                                            </svg>
                                        </button></div>
                                        <div v-else>
                                        <button type="button" @click="like(post.post_id,index)" class="btn btn-secondary">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                fill="currentColor" class="bi bi-suit-heart" viewBox="0 0 16 16">
                                                <path
                                                    d="m8 6.236-.894-1.789c-.222-.443-.607-1.08-1.152-1.595C5.418 2.345 4.776 2 4 2 2.324 2 1 3.326 1 4.92c0 1.211.554 2.066 1.868 3.37.337.334.721.695 1.146 1.093C5.122 10.423 6.5 11.717 8 13.447c1.5-1.73 2.878-3.024 3.986-4.064.425-.398.81-.76 1.146-1.093C14.446 6.986 15 6.131 15 4.92 15 3.326 13.676 2 12 2c-.777 0-1.418.345-1.954.852-.545.515-.93 1.152-1.152 1.595L8 6.236zm.392 8.292a.513.513 0 0 1-.784 0c-1.601-1.902-3.05-3.262-4.243-4.381C1.3 8.208 0 6.989 0 4.92 0 2.755 1.79 1 4 1c1.6 0 2.719 1.05 3.404 2.008.26.365.458.716.596.992a7.55 7.55 0 0 1 .596-.992C9.281 2.049 10.4 1 12 1c2.21 0 4 1.755 4 3.92 0 2.069-1.3 3.288-3.365 5.227-1.193 1.12-2.642 2.48-4.243 4.38z" />
                                            </svg>
                                        </button></div>
                                        <form @submit.prevent="comment(post.post_id)">
                                            <div class="cols-md-3">
                                                <label for="message-text" class="col-form-label">Comment:</label>
                                                <textarea v-model="content" class="form-control"
                                                    id="message-text"></textarea>
                                            </div>
                                            <button type="submit" class="btn btn-primary">comment</button>
                                        </form>
                                        <p class=""><small class="text-body-secondary">{{ post.timestamp }}
                                            </small></p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import NavBar from '@/components/nav.vue'
export default {
    name: 'NewsFeed',
    data() {
        return {
            user_id:localStorage.getItem('user_id'),
            posts: {},
            content: '',
            comments: {},
            following: []
        }
    },
    components: {
        NavBar,
    },
    computed: {
        modalTarget() {
            return function (id) {
                return "#" + 'a' + id;
            }
        },
        Id() {
            return function (id) {
                return "a" + id;
            }
        }
    },

    mounted() {
        fetch("http://127.0.0.1:8000/api/posts/" + "0", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                Authorization: "Bearer " + localStorage.getItem("access_token"),
            },
        })

            .then((response) => {
                console.log(response)
                return response.json();
            })
            .then((data) => {
                console.log(data)
                this.posts = data;
            })
        fetch("http://127.0.0.1:8000/api/follow/" + localStorage.getItem('user_id') + '/False', {
            headers: {
                "Access-Control-Allow-Origin": "*",
                Authorization: "Bearer " + localStorage.getItem("access_token")
            },
            method: "GET",
        })
            .then((response) => {
                return response.json()
            })
            .then((data) => {
                // console.log(data.accounts[0]['following'])
                const temp = data.accounts;
                temp.forEach(element => {
                    console.log(element['following'])
                    this.following.push(element['following'])
                });
            })
    },
    methods: {
        loadComment(p_id) {
            fetch("http://127.0.0.1:8000/api/comment/" + p_id, {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem("access_token")
                },
                method: "GET"
            })
                .then((response) => {
                    console.log(response)
                    return response.json();
                })
                .then((data) => {
                    console.log(data)
                    this.comments = data;
                })
        },

        like(p_id,index){
            this.posts[index].liked_by.push(localStorage.getItem('user_id'))
            fetch("http://127.0.0.1:8000/api/like", {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem("access_token")
                },
                method: "POST",
                body:
                    JSON.stringify({
                        'id': p_id
                    })
            })
                .then((response) => {
                    if (response.ok) {
                        alert('commented')
                        this.content = ''
                        this.loadComment(p_id)
                    }
                    return response.json()
                })
        },
        unlike(p_id,index){
            // console.log()
            this.posts[index].liked_by= this.posts[index].liked_by.filter(x => x != localStorage.getItem('user_id'))
            fetch("http://127.0.0.1:8000/api/like", {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem("access_token")
                },
                method: "DELETE",
                body:
                    JSON.stringify({
                        'id': p_id
                    })
            })
                .then((response) => {
                    if (response.ok) {
                        alert('commented')
                        this.content = ''
                        this.loadComment(p_id)
                    }
                    return response.json()
                })
        },





        comment(p_id) {
            fetch("http://127.0.0.1:8000/api/comment", {

                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem("access_token")
                },
                method: "POST",
                body:
                    JSON.stringify({
                        'comment': this.content,
                        'user_id': localStorage.getItem('user_id'),
                        'post_id': p_id
                    })
            })
                .then((response) => {
                    if (response.ok) {
                        alert('commented')
                        this.content = ''
                        this.loadComment(p_id)
                    }
                    return response.json()
                })
        }
    }

}
</script>
<style>
.sdw {
    width: 1000px;
    transition: width 0.2s;
}

.sdw:hover {

    width: 1010px;
    border-radius: 10px;
    /* box-shadow: rgba(205, 205, 209, 0.719) 10px 13px 27px -5px, rgba(219, 214, 214, 0.678) 5px 8px 16px -8px inset; */

}
</style>