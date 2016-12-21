/*jshint multistr: true */

var phoneloginid = '';

function logout() {
    $.ajax({
        type: 'POST',
        url: 'f/loginout/logout',
        async:false,
        data: {},
        success:
            function (returnedData) {
                location.reload();
            }
    });
}

function checkmail() {
    $.ajax({
        type: 'POST',
        url: 'f/parsers/checkmail',
        async:false,
        data:   {
                'e':$('#signuppage #email').val()
            },
        success:
            function (returnedData) {
                if (returnedData == 'True') {
                    $('#signuppage #email').attr('class', "True");
                } else {
                    $('#signuppage #email').attr('class', "False");
                    $('#signuppage #errorstatus').html(returnedData);
                }
            }
    });
}

function signup() {
    if($('#signuppage #password1').val() != $('#signuppage #password2').val()) {
        $('#signuppage #errorstatus').html("Passwords do not match.");
    }
    $("#signuppage button").attr('class','off');
    $.ajax({
        type: 'POST',
        url: 'f/editors/signup',
        async: true,
        data:   {
                'e':$('#signuppage #email').val(),
                'p':$('#signuppage #password1').val(),
				'loginid':phoneloginid
            },
        success:
            function (returnedData) {
				console.log(returnedData);
                if(returnedData == 'True') {
                    location.reload();
                } else {
                    $('#signuppage #errorstatus').html(returnedData);
                    $("#signuppage button").attr('class','');
                }
            }
    });
}

function login() {
    if (page != 'login') {
        return false;
    }
    $("#loginpage button").attr('class','off');
    $.ajax({
        type: 'POST',
        url: 'f/loginout/login',
        async: true,
        data:   {
                'e':$('#loginpage #email').val(),
                'p':$('#loginpage #password').val(),
				'loginid':phoneloginid
            },
        success:
            function (returnedData) {
                if (returnedData != '0' && !isNaN(returnedData)) {
                    location.reload();
                } else {
                    $("#loginpage button").attr('class','');
                    if (returnedData == '0') {
                        $('#loginpage #errorstatus').html("login failed");
                    } else {
                        $('#loginpage #errorstatus').html(returnedData);
                    }
                }
            }
    });
}

function resetpass() {
	if (page != 'login') {
        return false;
    }
	$("#loginpage button").attr('class','off');
    $.ajax({
        type: 'POST',
        url: 'f/editors/newpass',
        async: true,
        data:   {
                'e':$('#loginpage #email').val(),
            },
        success:
            function (returnedData) {
                if (returnedData == 'v') {
					$('#loginpage').html(
				        '<div class="form">\
				            <img src="static/images/loading.png">\
				            <h2>Sent</h2>\
							<span>Check your email for a reset password request.</span>\
				        </div>');
                } else {
					$("#loginpage button").attr('class','');
	                if (returnedData == '0') {
	                    $('#loginpage #errorstatus').html("login failed");
	                } else {
	                    $('#loginpage #errorstatus').html(returnedData);
	                }
                }
            }
    });
}

function forgotpass() {
	if (page != 'login') {
        return false;
    }
    $("#loginpage button").attr('class','off');
    $.ajax({
        type: 'POST',
        url: 'f/editors/forgotpass',
        async: true,
        data:   {
                'e':$('#loginpage #email').val(),
            },
        success:
            function (returnedData) {
                if (returnedData == 'v') {
					$('#loginpage').html(
				        '<div class="form">\
				            <img src="static/images/loading.png">\
				            <h2>Sent</h2>\
							<span>Check your email for a reset password request.</span>\
				        </div>');
                } else {
					$("#loginpage button").attr('class','');
	                if (returnedData == '0') {
	                    returnedData = "incorrect address";
	                }
					$('#loginpage #errorstatus').html(returnedData);
                }
            }
    });
}

function resetpass() {
	if (page != 'login') {
        return false;
    }
	$("#loginpage button").attr('class','off');
    $.ajax({
        type: 'POST',
        url: 'f/editors/newpass',
        async:false,
        data:   {
                'p':$('#loginpage #password').val(),
				'key':urlvars.resetpass,
				'id':urlvars.id
            },
        success:
            function (returnedData) {
                if (returnedData == 'v') {
					$('#loginpage').html(
				        '<div class="form">\
				            <img src="static/images/loading.png">\
				            <h2>Done</h2>\
							<span>You can now login with your new password.</span>\
				        </div>');
                } else {
					$("#loginpage button").attr('class','');
	                if (returnedData == '0') {
	                    returnedData = "bad password";
	                }
	                $('#loginpage #errorstatus').html(returnedData);
                }
            }
    });
}

function forgotpassform() {
    $('#loginpage').html(
        '<div class="form">\
            <img src="static/images/loading.png">\
            <h2>forgot password</h2>\
            <span id="errorstatus"></span>\
            <div>\
                <span>email</span> <input id="email" type="email" placeholder="email">\
            </div>\
            <button onmousedown="forgotpass()">Send</button><span class="forgotpass" onclick="loginform()">back</span>\
        </div>'
    );
}
function resetpassform() {
	$('#loginpage').html(
        '<div class="form">\
            <img src="static/images/loading.png">\
            <h2>reset password</h2>\
            <span id="errorstatus"></span>\
            <div>\
                <span>password</span> <input id="password" type="password" placeholder="password">\
            </div>\
            <button onmousedown="resetpass()">Send</button><span class="forgotpass" onclick="loginform()">back</span>\
        </div>'
    );
}
function loginform() {
    $('#loginpage').html(
        '<div class="form">\
            <img src="static/images/loading.png">\
            <h2>Login</h2>\
            <span id="errorstatus"></span>\
            <div>\
                <span>email</span> <input id="email" type="email" placeholder="email">\
            </div>\
            <div>\
                <span>password</span> <input id="password" type="password" placeholder="password">\
            </div>\
            <button onmousedown="login()">Login</button><span class="forgotpass" onclick="forgotpassform()">forgot password</span>\
        </div>'
    );
}
function signupform() {
    $('#signuppage').html(
        '<div class="form">\
            <img src="static/images/loading.png">\
            <h2>Signup</h2>\
            <span id="errorstatus"></span>\
            <div>\
                <span>email</span> <input id="email" type="email" placeholder="email" onblur="checkmail()">\
            </div>\
            <div>\
                <span>password</span> <input id="password1" type="password" placeholder="password">\
            </div>\
            <div>\
                <span>confirm password</span> <input id="password2" type="password" placeholder="confirm password">\
            </div>\
            <button onmousedown="signup()">Signup</button>\
        </div>'
    );
}
