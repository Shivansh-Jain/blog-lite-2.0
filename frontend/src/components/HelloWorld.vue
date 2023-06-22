<template>
  <body width="100%" height="100%">
  <h2 style="text-align: center;padding-top: 1cm;color: white;">Blog Lite Application</h2>
  <main class="form-signin w-100 m-auto" style="max-width: 35%;padding-top: 2cm;">
      <form @submit.prevent="login" method="POST">

          <h1 class="h3 mb-3 fw-normal" style="padding-bottom: 0.2cm;color: white;">Please sign in</h1>

          <div class="form-floating" style="padding-bottom:0.1cm ;">
              <input v-model="email" type="email" class="form-control" name="user_id" placeholder="name@example.com">
              <label for="floatingInput">Email address</label>
              
          </div>
          <div class="form-floating" style="padding-bottom:0.1cm ;">
              <input v-model="password" type="password" class="form-control" name="password" placeholder="Password">
              <label for="floatingPassword">Password</label>
          </div>

          <button class="w-100 btn btn-lg btn-primary" style="margin-bottom: 0.1cm;" type="submit">Sign in</button>
          <!-- {% if alert == "wrong" %}
          <div class="alert alert-primary" style="height:1.2cm" role="alert">
              <p style="vertical-align: middle;">Incorrect password is please try again.</p>
          </div>
          {%elif alert == 'create'%}
          <div class="alert alert-primary" style="height:1.2cm" role="alert">
              <p style="vertical-align: middle;">User didn't exist please click on create account to sign up.</p>
          </div>
          {%endif%} -->
      </form>
      <p class="mt-3">
              Not a member? <router-link to="/signup">Create a new Account</router-link>
          </p>
  </main>

</body>
</template>

<script>
// import router from routes
export default {
  name: "LoginForm",
  data(){
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
              fetch("/api/login",{
                  method:"POST",
                  headers:{
                      "Content-Type": "application/json",
                      "Access-Control-Allow-Origin":"*",
                  },
                  body: JSON.stringify({
                      username: this.username,
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
                      localStorage.setItem("username",this.username);
                      this.$router.push('/');
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