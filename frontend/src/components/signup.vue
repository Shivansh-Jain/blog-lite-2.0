<template>

    <main class="form-signin w-100 m-auto" style="max-width: 35%;padding-top: 2cm;">
        <form @submit.prevent="signup" method="POST" enctype="multipart/form-data">
            <h1 class="h3 mb-3 fw-normal" style="color: white;">Sign Up</h1>
            <div class="form-floating" style="padding-bottom:0.1cm ;">
                <input v-model="fname" class="form-control" name="fname" placeholder="First Name">
                <label for="floatingfname">First Name</label>
                <div class="alert alert-danger p-1" role="alert" v-if="v$.fname.$error">
                    First Name is required.
                </div>
            </div>
            <div class="form-floating" style="padding-bottom:0.1cm;">
                <input v-model="lname" class="form-control" name="lname" placeholder="Last Name">
                <label for="floatinglname">Last Name</label>
            </div>
            <div class="form-floating" style="padding-bottom:0.1cm ;">
                <input v-model="user_id" class="form-control" name="user_id" placeholder="Email Address" >
                <label for="floatinguser_id">Email Address</label>
                <div class="alert alert-danger p-1" role="alert" v-if="v$.user_id.$error">
                    Please enter valid email
                </div>
            </div>
            <div class="form-floating" style="padding-bottom:0.1cm ;">
                <input v-model="password" class="form-control" name="password" type='password' placeholder="New Password" >
                <label for="floatingpassword">Password</label>
                <div class="alert alert-danger p-1" role="alert" v-if="v$.password.$error">
                    Password is required and should have atleast 6 characters
                </div>
            </div>
            <div class="form-floating" style="padding-bottom:0.1cm ;">
                <input v-model="repassword" class="form-control" name="password" type='password' placeholder="New Password" >
                <label for="floatingpassword">Re-enter Password</label>
                <div class="alert alert-danger p-1" role="alert" v-if="v$.repassword.$error">
                    Password does not match.
                </div>
            </div>


            <div class="form-floating mb-1">
                <div class="form-control pt-0 pb-5"><p style="margin-bottom: 0.2cm;">Profile Picture</p>
                    <input @change="handle_image" ref="profile" name="profile"  type="file" accept="image/jpeg,image/png"></div>
            </div>
            <!-- </div>  -->
            <button class="btn btn-lg btn-primary" type="submit" style="width: 100%;">Create Account</button>
        </form>
        <p class="mt-3">
                Already a member? <router-link to="/login">Sign In</router-link>
            </p>

        <div class="danger" v-if="errStatus">{{ errormsg }}</div>
</main>

</template>
<script>
// import { required, email } from '@vuelidate/validators'
import { useVuelidate } from '@vuelidate/core'
import { required, minLength, sameAs, email } from "@vuelidate/validators";
import router from '@/router'
// import { file } from '@babel/types';
export default{
    setup () {
    return { v$: useVuelidate() }
  },
    name:"CreateForm",
    data(){
        return {
            fname:"",
            lname:"",
            user_id:"",
            password:"",
            repassword:"",
            errormsg:"",
            errStatus:false,
            profile:null
            
        };
    },
    validations() {
        return{
        fname: { required,$autoDirty:true },
        user_id : {required,email,$autoDirty:true},
        password:{required,minLength:minLength(6),$autoDirty:true},
        repassword:{sameAsPassword:sameAs(this.password),$autoDirty:true},
    }},
    methods:{
        handle_image(){
            this.profile=this.$refs.profile.files[0];
        },
        signup(){
            console.log("before touch");
            console.log(this.v$);
            this.v$.$validate()
            if (!this.v$.$error){
                console.log('entered')
                const formData=new FormData();
                formData.append('user_id',this.user_id);//event.target.elements.user_id.value);
                formData.append('password',this.password);//event.target.elements.password.value);
                formData.append('name',this.fname+' '+this.lname);//event.target.elements.fname.value+' '+event.target.elements.lname.value);
                formData.append('profile',this.profile);
            console.log(formData);
            fetch("http://127.0.0.1:8000/api/accounts",{
                method:"POST",
                
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

            if (data.status){
            localStorage.setItem("access_token",data.access_token);
            localStorage.setItem("user_id",this.user_id);
            localStorage.setItem('username',this.fname+" "+this.lname)
            router.push('/newsfeed');
        } else {
            this.errStatus = true;
            this.errormsg=data.message;
            this.fname='';
            this.lname='';
            this.user_id=null;
            this.password=null;
            this.repassword=null;
        }
        })
        .catch((err) =>{
            console.log(err);
        })
        }
    }
}
}
</script>