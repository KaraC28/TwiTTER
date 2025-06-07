function loadDoc(url, func){
    let xhttp = new XMLHttpRequest();
    xhttp.onload = function(){
        if (xhttp.status != 200){
            console.log("Error");
        }
        else{
            func(xhttp.response);
        }
    }
    xhttp.open("GET", url);
    xhttp.send();
}
///////////////////////////////////////////////////Code for profile///////////////////////////////////////////////////////
/* Getting rid of this cuz putting it in the template seems easier
function userProfile(){ //what shows up when the user is on their profile
    url = '/twitter/profile/<username>';
    loadDoc(url, userProfile_response); //gotta figure out passing the username...
}
function userProfile_response(response){ //hope this is ok??
    let data = JSON.parse(response);
    let result = data["profileResults"];

    console.log(session_username + " is logged in");
    console.log(session_user_id);

    let temp = "";
    for (let i = 0; i < results.length; i++){
        //username and pfp stuff
        //let row = results[i];
        //if (session_username == row["username"]){ //if current session username matches with username found in JSON
            //temp = "<div>";
        temp = "<div id = 'profilePic'>";
        //temp = row["profilePic"] + "<br/>";     come back to this later
        temp = "</div>";
            //temp = "<button onclick='uploadPfp();'> Upload new pfp </button>";
        temp = "<b>" + row["username"]+ "</b>" + "<br/>";
        temp = "<input type = 'text' id = 'userPost'/>" + "<br/>";
        temp = "<button onclick='newPost(session_user_id);'> New Post </button>";
            //temp  = "</div>";
        //}

        //posts stuff

        let posts = row["posts"];
        for (let i = 0; i < posts.length; i++){
            let post = posts[i];
            temp = "<div>";
            temp = "<b>" + row["username"]+ "</b>" + "<br/>";
            temp = post["text"] + "<br/>";
            temp = post["date"] + "<br/>"; //will work on reply button later
            temp  = "</div>";
        }
    }
    let profile = document.getElementById("profile");
    profile.innerHTML = temp;
}
function someoneProfile(){
    url = '/twitter/profile/<username>';
    loadDoc(url, someoneProfile_response); //gotta figure out passing the username...
}

function someoneProfile_response(response){ //what shows up when you're on someone else's profile
    let data = JSON.parse(response);
    let result = data["profileResults"];

    console.log(session_username + " is logged in");
    console.log(session_user_id);

    let temp = "";
    for (let i = 0; i < results.length; i++){
        //username and pfp stuff
        //let row = results[i];
        //if (session_username == row["username"]){
        //temp = "<div>";
        temp = "<div id = 'profilePic'>";
        //temp = row["profilePic"] + "<br/>"; //this will be put back in later
        temp = "</div>";
        temp = "<b>" + row["username"]+ "</b>" + "<br/>";
        //temp  = "</div>";
        //}
        //posts stuff

        let posts = row["posts"];
        for (let i = 0; i < posts.length; i++){
            let post = posts[i];
            temp = "<div>";
            temp = "<b>" + row["username"]+ "</b>" + "<br/>";
            temp = post["text"] + "<br/>";
            temp = post["date"] + "<br/>"; //will work on reply button later
            temp  = "</div>";
        }
    }
    let profile = document.getElementById("profile");
    profile.innerHTML = temp;
} */

function newPost(){
    let xhttp = new XMLHttpRequest();
    xhttp.onload = function(){
        if (xhttp.status != 200){
            console.log("Error");
        }
        else{
            newPost_response(xhttp.response);
        }
    }
    url = "/twitter/profile/addPost";
    xhttp.open("POST", url , true);

    var formData = new FormData();
    formData.append("user_id", session_user_id);
    //formData.append("user_id", user_id);
    formData.append("text", document.getElementById("userPost").value);
    xhttp.send(formData);
    //let post = document.getElementById("post");
    //let postId = document.getElementById("postId");

    //let url = "/newPost?post=" + post.value + "&postId=" + postId.value;
    //alert(url) //temporary
}

function newPost_response(response){
    location.reload();
}

function uploadPfp(){
    let xhttp = new XMLHttpRequest();
    xhttp.onload = function(){
        if (xhttp.status != 200){
            console.log("Error");
        }
        else{
            uploadPfp_response(xhttp.response);
        }
    }
    url = "/twitter/profile/uploadImage";
    xhttp.open("POST", url , true); //maybe use set item instead?

    var formData = new FormData();
    formData.append("file", document.getElementById("chooseFile").files[0]);
    xhttp.send(formData);

}
function uploadPfp_response(response){
    location.reload();
}

function showPfp(user_id){
    loadDoc("/twitter/profile/showPfp?user_id=" + user_id, showPfp_response);
}

function showPfp_response(response){
    let data = JSON.parse(response);
    let results = data["results"]; //results from image
    let url = data["url"]; //image url
    let items = data["items"]; //list of images in database
    let html = "";


    html += "<div>" + "<img src= \"" + url + items[0] + "\">" + "<br/>"; //items[0] has image key

    let profilePic = document.getElementById("profilePic");
    profilePic.innerHTML = html;
}

function listProfilePosts(profile_username){
    //loadDoc("/twitter/profile/listProfilePosts", listProfilePosts_response);
    //testing
    loadDoc("/twitter/profile/listProfilePosts?username=" + profile_username, listProfilePosts_response);
}
function listProfilePosts_response(response){
    let data = JSON.parse(response);
    let result = data["results"];

    let temp = "";
    for (let i = 0; i < result.length; i++){
        let row = result[i];
            temp += "<div>";
            temp += "<b>" + profile_username + "</b>" + "<br/>";
            temp += row["text"] + "<br/>";
            temp += row["date"] + "<br/>";
            temp  += "</div>";
    }
    let listProfilePosts = document.getElementById("listProfilePosts");
    listProfilePosts.innerHTML = temp;
}

////////////////////////////////////////////////////////////////Codes for the login/////////////////////////////////////////////////

function login(){
    let txtEmail = document.getElementById("txtEmail");
    let txtPassword = document.getElementById("txtPassword");
    let chkRemember = document.getElementById("chkRemember");

    let URL = "/twitter/login?email=" + txtEmail.value + "&password=" + txtPassword.value;
    if(chkRemember.checked){
        URL += "&remember=yes";
    }else{
        URL += "&remember=no";
    }

    loadDoc(URL, login_response);
}

function login_response(response){
    let data = JSON.parse(response);
    let result = data["result"];
    if(result != 'OK'){
        alert(result);
    }else{
        //window.location.replace('/profile.html');
        window.location.replace('/twitter/profile/' + data['username']);
    }
}

///////////////////////////////////////////////////////////////////////Codes for Signup////////////////////////////////////////

function signup(){
    let txtEmail = document.getElementById("txtNewEmail");
    let txtUsername = document.getElementById("txtNewUsername");
    let txtPassword = document.getElementById("txtNewPassword");

    let URL = "/twitter/signup?email=" + txtEmail.value + "&username=" + txtUsername.value + "&password=" + txtPassword.value;

    loadDoc(URL, signup_response);
}

function signup_response(response){
    let data = JSON.parse(response);
    let result = data["result"];
    if(result != 'OK'){
        alert(result);
    }
    else{
        //window.location.replace('/profile.html')
        window.location.replace('/twitter/profile/' + data['username']);
    }
}
////////////////////////////////////////////////Feed Code///////////////////////////////////////////////////

function list_posts(){
    let URL = '/twitter/list_posts';
    loadDoc(URL, list_posts_response);
}

function list_posts_response(response){
    let data = JSON.parse(response);
    let posts = data.posts;
    let temp = "";

    if(posts && posts.length > 0){
        for(let i = 0; i < posts.length; i++){
            let post = posts[i];
            temp += '<div class= "list_post">';

            temp+= '<div class= "postHeader">';
            //temp +='<div class="username" onclick="window.location.href=\'/profile/' + post.username + '\'">' + post.username + '</div>';
            //temp += '<button onclick="window.location.href=\'/post.html?id=' + post.TPostID + '\'">Comment</button>';

            temp+= '<a class="username" href="/profile/' + post.username + '">@' + post.username + '</a>';
            temp+= '</div>'; //close postHeader

            temp+= '<p class= "text">' + post.text + '</p>';

            temp += '<div class= "post_footer">';
            temp+= '<p class= "date">' + post.date + '</p>';
            temp += '<button onclick="window.location.href=\'/post.html?id=' + post.TPostID + '\'">Comment</button>';
            temp+= '</div>'; //closes post_footer

            temp+= '</div>'; //closes list_post
        }
    }
    else{
        temp += '<p>No recent post have been made</p>';
    }
    temp += "<a href = '/twitter/profile/" + data.session_username + "'>Back to your profile</a>";
    let divPosts = document.getElementById("listPosts");
    divPosts.innerHTML= temp;
}
///////////////////////////////////////////////Post View Codes////////////////////////////////////////////////////

function post_view(){
    let urlParams = new URLSearchParams(window.location.search);
    let postID = urlParams.get("id");

    let URL = '/twitter/post?id=' + postID;
    loadDoc(URL, post_view_response);
}

function post_view_response(response){
    let data= JSON.parse(response);
    let post = data.post;
    let replies = data.replies;

    let postContainer = document.getElementById("postContainer");
    let replyContainer = document.getElementById("repliesContainer");

    //display the parent post//

    let temp = "";

    temp += '<div class= "list_post">';
    temp += '<div class= "postHeader">';
    temp += '<a class= "username" href= "/profile/'+ post.username + '">@' + post.username + '</a>';
    temp += '<p class="date">' + post.date + '</p>';
    temp += '</div>';
    temp += '<p class="text">' + post.text + '</p>';
    temp += '</div>';

    postContainer.innerHTML = temp;

    //Display replies//

    let replyTemp = "<h3>Replies</h3>";
    if (replies.length > 0){
        for(let i=0; i < replies.length; i++){
            let reply = replies[i];
            replyTemp += '<div class= "list_post">';
            replyTemp += '<a class= "postHeader">';
            replyTemp += '<div class= "username" href="/profile/'+ reply.username + '">' + reply.username + '</a>';
            replyTemp += '<p class="date">' + reply.date + '</p>';
            replyTemp += '</div>';
            replyTemp += '<p class="text">' + reply.text + '</p>';
            replyTemp += '</div>';
        }
    }else{
        replyTemp += '<p>No replies yet</p>';
    }

    replyContainer.innerHTML = replyTemp;

}

function reply(){
    let urlParams = new URLSearchParams(window.location.search);
    let postID = urlParams.get("id");
    let replyText = document.getElementById("replyInput").value;

    let xhttp = new XMLHttpRequest();
    xhttp.onload = function(){
        if(xhttp.status !=200){
            console.log("Error submitting reply");
        }
        else{
            location.reload();//show new reply
        }
    };

    let URL = "/twitter/post/reply";
    xhttp.open("POST", URL, true);

    let formData = new FormData();
    formData.append("parent_id", postID);
    formData.append("text", replyText);
    xhttp.send(formData);
}