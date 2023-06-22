<template>

    <h2 style="text-align: center;padding-top: 1cm;color: white;">Blog Lite Application</h2>
    <main class="form-signin w-100 m-auto" style="max-width: 35%;padding-top: 2cm;">
        <form @submit.prevent="login" method="POST">
            <div v-if="errStatus">
            <br />
            <p class="alert alert-danger">{{ errormsg }}</p>
            </div>

            <h1 class="h3 mb-3 fw-normal" style="padding-bottom: 0.2cm;color: white;">Please sign in</h1>

            <div class="form-floating" style="padding-bottom:0.1cm ;">
                <input v-model="email" type="email" class="form-control" name="user_id" placeholder="name@example.com" required>
                <label for="floatingInput">Email address</label>
                <!-- <div class="error" v-if="!$v.email.required">
                    Email Address is required
                </div>
                 -->
            </div>
            <div class="form-floating" style="padding-bottom:0.1cm ;">
                <input v-model="password" type="password" class="form-control" name="password" placeholder="Password">
                <label for="floatingPassword">Password</label>
                <!-- <div class="error" v-if="!$v.password.required">
                    Password is required
                </div> -->
            </div>

            <button class="w-100 btn btn-lg btn-primary btn-change8" style="margin-bottom: 0.1cm;" type="submit">Sign in</button>
        </form>
        <p class="mt-3">
                Not a member? <router-link to="/signup">Sign up</router-link>
            </p>
    </main>


</template>

<script>
// import router from routes
export default {
    name: "LoginForm",
    data:function(){
        return {
            email:"",
            password:"",
            errormsg:"",
            errStatus:false,
            
        };
    },
    
    methods:{
        login(){
            if (this.email && this.password){
                fetch("http://127.0.0.1:8000/api/login",{ 
                    method:"POST",       
                    headers:{
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin":"*",
                        
                    },
                    body: JSON.stringify({
                        user_id: this.email,
                        password: this.password,
                    }),
                })
                .then((response) => {
                    if (!response.ok){
                        alert("Respnse not ok");
                    }
                    return response.json();
                })
                .then((data) => {
                    console.log(data.msg);
                    if (data.status){
                        localStorage.setItem("access_token",data.access_token);
                        localStorage.setItem("user_id",this.email);
                        localStorage.setItem('username',data.username)
                        // alert("login successfull")
                        this.$router.push('/newsfeed');
                    } else {
                        this.errStatus = true;
                        this.errormsg = data.msg;
                        this.username = null;
                        this.password = null;
                    }
                })
                .catch((err) => {
                    console.log(err);
                });
            }
        },
    },
};
</script>
