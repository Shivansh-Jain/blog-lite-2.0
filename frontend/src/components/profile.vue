<template>
    <NavBar></NavBar>
    <!-- nav bar -->
    <div class="card px-3 pt-3 m-auto" style="max-width: 40rem;background-color:#EAF4FF;margin-top: 1rem !important;">
        <!-- <div class="row d-flex justify-content-center align-items-center h-100"> -->
        <div class="col col-lg-9 col-xl-7" style="width: 100%;align-items: center;">
            <div class="card">
                <div class="rounded-top text-white d-flex flex-row" style="background-color: #000; height:200px;">
                    <div class="ms-4 mt-5 d-flex flex-column" style="width:30%">
                        <img :src="require(`@/assets/profile/${user_id}.jpg`)" alt="Generic placeholder image"
                            class="img-fluid img-thumbnail mt-4 mb-2" style="width: 100%;height: 2.5cm; ">
                    </div>
                    <div class="ms-3" style="margin-top: 130px;width: 38%;">
                        <h5>{{ username }}</h5>
                    </div>
                    <div width="32%">
                        <a href="" style="width: 22%;height: 25%;">
                            <button type="button" @click="delete_prof" class="btn btn-danger position-absolute top-10 end-0"
                                onclick="return confirm('Are you sure you want to delete your account?');">
                                Delete Profile
                            </button></a>


                        <button type="button" class="btn btn-primary" style="width: 100%;margin-top: 112%"
                            data-bs-toggle="modal" data-bs-target="#update_p">
                            Update Profile
                        </button>
                        <div class="modal fade" id="update_p" tabindex="-1" aria-labelledby="exampleModalLabel"
                            aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h1 class="modal-title fs-5" id="exampleModalLabel">Edit Profile</h1>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal"
                                            aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                        <form @submit.prevent="update_profile" method="POST" enctype="multipart/form-data">

                                            <div class="form-floating" style="padding-bottom:0.1cm ;">
                                                <input v-model="fname" class="form-control" name="fname"
                                                    placeholder="First Name">
                                                <label for="floatingfname">First Name</label>
                                                <div class="alert alert-danger p-1" role="alert" v-if="v$.fname.$error">
                                                    First Name is required.
                                                </div>
                                            </div>
                                            <div class="form-floating" style="padding-bottom:0.1cm;">
                                                <input v-model="lname" class="form-control" name="lname"
                                                    placeholder="Last Name">
                                                <label for="floatinglname">Last Name</label>
                                            </div>
                                            <div class="form-floating" style="padding-bottom:0.1cm ;">
                                                <input v-model="user_id" disabled class="form-control" name="user_id"
                                                    placeholder="Email Address">
                                                <label for="floatinguser_id">Email Address</label>
                                                <div class="alert alert-danger p-1" role="alert" v-if="v$.user_id.$error">
                                                    Please enter valid email
                                                </div>
                                            </div>
                                            <div class="form-floating" style="padding-bottom:0.1cm ;">
                                                <input v-model="password" class="form-control" name="password"
                                                    type='password' placeholder="New Password">
                                                <label for="floatingpassword">Password</label>
                                                <div class="alert alert-danger p-1" role="alert" v-if="v$.password.$error">
                                                    Password is required and should have atleast 6 characters
                                                </div>
                                            </div>
                                            <div class="form-floating" style="padding-bottom:0.1cm ;">
                                                <input v-model="repassword" class="form-control" name="password"
                                                    type='password' placeholder="New Password">
                                                <label for="floatingpassword">Re-enter Password</label>
                                                <div class="alert alert-danger p-1" role="alert"
                                                    v-if="v$.repassword.$error">
                                                    Password does not match.
                                                </div>
                                            </div>


                                            <div class="form-floating mb-1">
                                                <div class="form-control pt-0 pb-5">
                                                    <p style="margin-bottom: 0.2cm;">Profile Picture</p>
                                                    <input @change="handle_image" ref="profile" name="profile" type="file"
                                                        accept="image/jpeg,image/png">
                                                </div>
                                            </div>
                                            <!-- </div>  -->
                                            <button class="btn btn-lg btn-primary" type="submit" style="width: 100%;">Update
                                                Profile</button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="p-4 text-black" style="background-color: #f8f9fa;">
                <div class="d-flex justify-content-end text-center py-1">
                    <div>
                        <p class="mb-1 h5">{{ posts.length }}</p>
                        <p class="small text-muted mb-0">Posts</p>
                    </div>
                    <div class="px-3">
                        <p class="mb-1 h5">{{ followers.length }}</p>

                        <p class="small text-muted mb-0" data-bs-toggle="modal" data-bs-target="#follower">Followers</p>
                    </div>
                    <div class="modal fade" id="follower" tabindex="-1" aria-labelledby="exampleModalLabel"
                        aria-hidden="true">
                        <div class="modal-dialog">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h1 class="modal-title fs-5" id="exampleModalLabel">Followers</h1>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                                        aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <div class="container">
                                        <div v-for="acc in followers" v-bind:key="acc.user">
                                            <div class="row">
                                                <div class="col-sm-1">
                                                    <img :src="require(`@/assets/profile/${acc.user}.jpg`)"
                                                        style="border-radius: 50%;" width="40" height="40"
                                                        class="d-inline-block align-top" alt="">
                                                </div>
                                                <div class="col-sm-4">
                                                    <p>{{ acc.names }}</p>
                                                </div>
                                                <div class="col-sm-7">
                                                    <div v-if="c_following.includes(acc.user)">
                                                        <button type="button" class="btn btn-light"
                                                            @click="unfollow(acc.user)"
                                                            style="float: right;">Unfollow</button>
                                                    </div>
                                                    <div v-else>
                                                        <button type="button" class="btn btn-primary"
                                                            @click="follow(acc.user)" style="float: right;">Follow</button>
                                                    </div>

                                                </div>
                                            </div><br>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div>
                        <p class="mb-1 h5">{{ following.length }}</p>

                        <p class="small text-muted mb-0" data-bs-toggle="modal" data-bs-target="#following">Following</p>
                        <div class="modal fade" id="following" tabindex="-1" aria-labelledby="exampleModalLabel"
                            aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h1 class="modal-title fs-5" id="exampleModalLabel">Followers</h1>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal"
                                            aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                        <div class="container">
                                            <div v-for="acc in following" v-bind:key="acc.following">
                                                <div class="row">
                                                    <div class="col-sm-1">
                                                        <img :src="require(`@/assets/profile/${acc.following}.jpg`)"
                                                            style="border-radius: 50%;" width="40" height="40"
                                                            class="d-inline-block align-top" alt="">
                                                    </div>
                                                    <div class="col-sm-4">
                                                        <p>{{ acc.fnames }}</p>
                                                    </div>
                                                    <div class="col-sm-7">
                                                        <div v-if="c_following.includes(acc.following)">
                                                            <button type="button" class="btn btn-light"
                                                                @click="unfollow(acc.following)"
                                                                style="float: right;">Unfollow</button>
                                                        </div>
                                                        <div v-else>
                                                            <button type="button" class="btn btn-primary"
                                                                @click="follow(acc.following)"
                                                                style="float: right;">Follow</button>
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
                </div>
            </div>
            <div v-for="(post, index) in posts" v-bind:key="post.post_id" class="">
                <div class="row row-cols-2" data-bs-toggle="modal" :data-bs-target="modalTarget(post.post_id)"
                    @click="loadComment(post)">
                    <div class="col-md-3">
                        <img class="img-fluid" :src="require(`@/assets/posts/${post.post}`)" alt="Image" />
                    </div>
                    <div class="col-md-8">
                        <div class="card-body">
                            <h4 class="card-title" style="text-align: left;">{{ post.title }}</h4>
                            <p class="card-text"
                                style="text-align: left;max-height: 2cm;overflow: hidden;margin-bottom: 1cm;">{{
                                    post.caption }}</p>
                        </div>
                        <div class="card-footer">
                            <div class="row g-0">
                                <div class="col-md-2">
                                    <img class="img-fluid" :src="require(`@/assets/profile/${post.user_id}.jpg`)"
                                        style="height: 40px;width: 40px;border-radius: 20px;background-color: grey;" />
                                </div>
                                <div class="col-md-4" style="text-align: left;">
                                    <h5>{{ post.name }}</h5>
                                </div>
                                <div class="col" style="text-align: right;">
                                    <p class="card-text"><small class="text-body-secondary">{{ post.timestamp }}
                                        </small></p>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>
                <div class="modal fade" :id="Id(post.post_id)" tabindex="-1" aria-labelledby="pageLabel" aria-hidden="true">
                    <div class="modal-dialog  modal-xl">
                        <div class="modal-content">
                            <div class="row">
                                <h1 class="modal-title" id="pageLabel" :v-html="post.title">{{ post.title }}</h1>
                            </div>
                            <div class="row">
                                <img :src="require(`@/assets/posts/${post.post}`)" class="img-fluid rounded-start"
                                    alt="...">
                            </div>
                            <div class="row">
                                <p class=""><small class="text-body-secondary">{{ post.timestamp }}
                                        </small></p>
                            </div>
                            <div class="row">
                                <div class="d-flex justify-content-between">
                                    <h5 class="m-2" :v-html="post.caption">{{ post.caption }}</h5>
                                    <div>


                                        <button v-if="post.liked_by.includes(user_id)" @click="unlike(post.post_id, index)"
                                            type="button" class="btn btn-secondary">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                fill="currentColor" class="bi bi-suit-heart-fill" viewBox="0 0 16 16">
                                                <path
                                                    d="M4 1c2.21 0 4 1.755 4 3.92C8 2.755 9.79 1 12 1s4 1.755 4 3.92c0 3.263-3.234 4.414-7.608 9.608a.513.513 0 0 1-.784 0C3.234 9.334 0 8.183 0 4.92 0 2.755 1.79 1 4 1z" />
                                            </svg>
                                        </button>


                                        <button v-else type="button" @click="like(post.post_id, index)"
                                            class="btn btn-secondary">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                fill="currentColor" class="bi bi-suit-heart" viewBox="0 0 16 16">
                                                <path
                                                    d="m8 6.236-.894-1.789c-.222-.443-.607-1.08-1.152-1.595C5.418 2.345 4.776 2 4 2 2.324 2 1 3.326 1 4.92c0 1.211.554 2.066 1.868 3.37.337.334.721.695 1.146 1.093C5.122 10.423 6.5 11.717 8 13.447c1.5-1.73 2.878-3.024 3.986-4.064.425-.398.81-.76 1.146-1.093C14.446 6.986 15 6.131 15 4.92 15 3.326 13.676 2 12 2c-.777 0-1.418.345-1.954.852-.545.515-.93 1.152-1.152 1.595L8 6.236zm.392 8.292a.513.513 0 0 1-.784 0c-1.601-1.902-3.05-3.262-4.243-4.381C1.3 8.208 0 6.989 0 4.92 0 2.755 1.79 1 4 1c1.6 0 2.719 1.05 3.404 2.008.26.365.458.716.596.992a7.55 7.55 0 0 1 .596-.992C9.281 2.049 10.4 1 12 1c2.21 0 4 1.755 4 3.92 0 2.069-1.3 3.288-3.365 5.227-1.193 1.12-2.642 2.48-4.243 4.38z" />
                                            </svg>
                                        </button>

                                        <a class="m-2" data-bs-toggle="modal" data-bs-target="#editpost"><svg
                                                xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
                                                <path
                                                    d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z" />
                                            </svg></a>
                                        <a class="m-2" @click="delete_post(post.post_id)" title="Delete Post"><svg
                                                xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
                                                <path
                                                    d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5ZM11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H2.506a.58.58 0 0 0-.01 0H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1h-.995a.59.59 0 0 0-.01 0H11Zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5h9.916Zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47ZM8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5Z" />
                                            </svg></a>
                                    </div>

                                </div>

                            </div>
                            <div class="text-center m-3">
                                <div class="row ">
                                    <form @submit.prevent="comment(post.post_id)">
                                        <div class="d-flex">
                                            <input v-model="content" type="text" class="form-control" id="message-text" />
                                            <button type="submit" class="btn btn-primary">comment</button>
                                        </div>

                                    </form>
                                    
                                </div>
                                <div class="row m-2">
                                    <h3>Comments</h3>
                                    <div class="container m-3">
                                        <div v-for="com in comments" v-bind:key="com.comment_id">
                                            <div class="row">
                                                <div class="d-flex flex-row align-items-end">
                                                    <img class="img-fluid m-2"
                                                        :src="require(`@/assets/profile/${com.user_id}.jpg`)"
                                                        style="height: 30px;width: 30px;border-radius: 20px;background-color: grey;" />
                                                    <h5>{{ com.name }}</h5>
                                                </div>
                                                <div class="d-flex flex-row  justify-content-start">
                                                    <p class="m-2">{{ com.comment }}</p>
                                                </div>
                                                <hr />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
            <div class="modal fade" id="editpost" aria-hidden="true" aria-labelledby="edit post" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="edit post">Edit Post</h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <form @submit.prevent="edit_post(post.post_id)" style="max-width: 50%;padding-top: 5%;"
                                class="m-auto" enctype="multipart/form-data">
                                <div class="form-floating">
                                    <input class="form-control" v-model="title" name="title" placeholder="Title" required>
                                    <label for="floatingtitle">Title</label>
                                </div>
                                <div class="form-floating">
                                    <input v-model="caption" class="form-control" name="caption"
                                        placeholder="write your caption here">
                                    <label for="floatingcaption">Caption</label>
                                </div>
                                <div class="modal-footer">
                                    <button class="w-100 btn btn-lg btn-primary" type="submit">Submit</button>

                                </div>

                            </form>
                        </div>

                    </div>
                </div>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
        </div>
    </div>
</template>
<script>
import NavBar from '@/components/nav.vue'
import { useVuelidate } from '@vuelidate/core'
import { required, minLength, sameAs, email } from "@vuelidate/validators";
import router from '@/router'
export default {
    setup() {
        return { v$: useVuelidate() }
    },

    name: "UserProfile",
    data() {
        return {
            user_id: localStorage.getItem('user_id'),
            username: localStorage.getItem('username'),
            fname: localStorage.getItem('username').split(' ')[0],
            lname: localStorage.getItem('username').split(' ')[1],
            posts: {},
            comments: {},
            c_following: [],
            following: [],
            followers: [],
            password: "",
            repassword: "",
            errormsg: "",
            errStatus: false,
            profile: null,
            title: '',
            caption: ''
        }
    },
    validations() {
        return {
            fname: { required, $autoDirty: true },
            user_id: { required, email, $autoDirty: true },
            password: { required, minLength: minLength(6), $autoDirty: true },
            repassword: { sameAsPassword: sameAs(this.password), $autoDirty: true },
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
    beforeMount() {
        fetch("http://127.0.0.1:8000/api/posts/" + localStorage.getItem('user_id'), {
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
            }),
            fetch("http://127.0.0.1:8000/api/follow/" + localStorage.getItem('user_id') + '/False', {
                headers: {
                    "Content-Type": "application/json",
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
                    this.following = data.accounts;
                    this.following.forEach(element => {
                        console.log(element['following'])
                        this.c_following.push(element['following'])
                    });
                })

        fetch("http://127.0.0.1:8000/api/follow/" + localStorage.getItem('user_id') + '/True', {
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
                this.followers = data.accounts;
                // temp.forEach(element => {
                //     console.log(element['following'])
                //     this.following.push(element['following'])
                // });
            })
    },
    methods: {
        handle_image() {
            this.profile = this.$refs.profile.files[0];
        },
        update_profile() {
            this.v$.$validate()
            if (!this.v$.$error) {
                console.log('entered')
                const formData = new FormData();
                formData.append('user_id', this.user_id);//event.target.elements.user_id.value);
                formData.append('password', this.password);//event.target.elements.password.value);
                formData.append('name', this.fname + ' ' + this.lname);//event.target.elements.fname.value+' '+event.target.elements.lname.value);
                formData.append('profile', this.profile);
                console.log(formData);
                fetch("http://127.0.0.1:8000/api/accounts", {
                    method: "PUT",
                    headers: {
                        "Access-Control-Allow-Origin": "*",
                        Authorization: "Bearer " + localStorage.getItem("access_token")
                    },
                    body:
                        formData
                    //     JSON.stringify({
                    //     user_id: this.user_id,
                    //     password:this.password,
                    //     name:this.fname+' '+this.lname,
                    //     profile:this.imageUrl,
                    // }),
                })
                    .then((response) => {
                        // if (!response.ok){
                        //     alert(" ");
                        //     console.log(response.json());
                        // }
                        return response.json();
                    })
                    .then((data) => {
                        console.log(data)
                        localStorage.removeItem('username')
                            localStorage.setItem('username', this.fname + " " + this.lname)
                            window.location.reload()
                        if (data.status) {
                            localStorage.removeItem('username')
                            localStorage.setItem('username', this.fname + " " + this.lname)
                            window.location.reload()
                        } else {
                            this.errStatus = true;
                            this.errormsg = data.message;
                            this.fname = '';
                            this.lname = '';
                            this.user_id = null;
                            this.password = null;
                            this.repassword = null;
                        }
                    })
                    .catch((err) => {
                        console.log(err);
                    })
            }
        },



        delete_prof() {
            fetch("http://127.0.0.1:8000/api/accounts/" + localStorage.getItem('user_id'), {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem('access_token')
                },
                method: "DELETE",
            })
                .then((response) => {
                    if (response.ok) {
                        localStorage.clear()
                        router.push('/')
                    }
                })


        },
        follow(id) {
            fetch("http://127.0.0.1:8000/api/follow", {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem('access_token')
                },
                method: "POST",
                body: JSON.stringify({
                    following: id
                }),
            })
                .then((response) => {
                    if (response.ok) {

                        this.c_following.push(id)
                        // window.location.reload()

                    }
                    console.log(response)
                    return response.json()
                })

        },
        unfollow(id) {
            fetch("http://127.0.0.1:8000/api/follow", {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem('access_token')
                },
                method: "DELETE",
                body: JSON.stringify({
                    following: id
                }),
            })
                .then((response) => {
                    if (response.ok) {

                        this.c_following = this.c_following.filter(x => x != id)
                    }
                    console.log(response)
                    return response.json()
                })

        },

        loadComment(post) {
            this.title = post.title
            this.caption = post.caption
            fetch("http://127.0.0.1:8000/api/comment/" + post.post_id, {
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
        like(p_id, index) {
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

                        this.content = ''
                        this.loadComment(p_id)
                    }
                    return response.json()
                })
        },
        unlike(p_id, index) {
            // console.log()
            this.posts[index].liked_by = this.posts[index].liked_by.filter(x => x != localStorage.getItem('user_id'))
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

                        this.content = ''
                        this.loadComment(p_id)
                    }
                    return response.json()
                })
        },

        edit_post(p_id) {
            fetch("http://127.0.0.1:8000/api/posts", {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem("access_token")
                },
                method: "PUT",
                body:
                    JSON.stringify({
                        'title': this.title,
                        'caption': this.caption,
                        'post_id': p_id
                    })
            })
                .then((response) => {
                    if (response.ok) {
                        window.location.reload()
                    }
                    return response.json()
                })
        },
        delete_post(p_id) {
            fetch("http://127.0.0.1:8000/api/posts/" + p_id, {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem("access_token")
                },
                method: "DELETE"
            })
                .then((response) => {
                    if (response.ok) {
                        window.location.reload()
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

                        this.content = ''
                        this.loadComment(p_id)
                    }
                    return response.json()
                })
        }
    }
}


</script>