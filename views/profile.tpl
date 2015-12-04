<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="">
    <meta name="author" content="">
	<script src="/static/js/updateprof.js"></script>
	<script src="/static/js/jquery.js"></script>
	<script src="/static/js/sjcl.js"></script>
	<script src="/static/js/login.js"></script>
	<script src="/static/js/search.js"></script>
	

    <title>PetBay</title>

    <!-- Bootstrap Core CSS -->
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="/static/css/thumbnail-gallery.css" rel="stylesheet">

    <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
        <script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
    <![endif]-->

</head>

<body>

    <!-- Navigation -->
    <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
		
			<a class="navbar-brand" rel="home" href="/" title="PetBay">
				<img style="max-width:75px; margin-top: -7px;"
				 src="/static/css/aww/logotranssmall.png">
			</a>
            <!-- Brand and toggle get grouped for better mobile display -->
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="/">Front</a>
            </div>
            <!-- Collect the nav links, forms, and other content for toggling -->
            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                <ul class="nav navbar-nav">
                    <li>
                        <a href="/halloffame">Hall of Fame</a>
                    </li>
					% if email is not None:
                    <li>
                        <a href="/profile">Profile</a>
                    </li>
					% else:
					<li>
						<a data-toggle="modal" href="#regModal" data-backdrop="true" >Register</a>
					</li>
					% end
                </ul>
				<!--http://bootsnipp.com/snippets/featured/horizontal-login-form-in-navbar-with-prepend-->
				% if email is None:
				<form id="signin" class="navbar-form navbar-right" role="form">
					<div class="input-group">
						<span class="input-group-addon"><i class="glyphicon glyphicon-user"></i></span>
						<input id="email" type="email" class="form-control" name="email" value="" placeholder="Email Address">                                        
					</div>

					<div class="input-group">
						<span class="input-group-addon"><i class="glyphicon glyphicon-lock"></i></span>
						<input id="password" type="password" class="form-control" name="password" value="" placeholder="Password">                                        
					</div>

					<button type="submit" onclick="login1(event)" class="btn btn-primary">Login</button>
				</form>
				% else:
				<form id="signout" class="navbar-form navbar-right" role="form" style="color:azure">
					Logged in as:&nbsp;{{email}}
					<button type="submit" onclick="logout(event)" class="btn btn-primary">Logout</button>
				</form>
				% end
            <!-- /.navbar-collapse -->
        </div>
        <!-- /.container -->
    </nav>
	<!-- Modal for Register-->
	<div id="experiment" class="modal fade" role="dialog" tabindex="-1" aria-labelledby="myModalLabel" aria-hidden="true"></div>
	<!--http://bootsnipp.com/snippets/8VmZ-->
	<div id="regModal" class="modal fade" role="dialog" tabindex="-1" aria-labelledby="myModalLabel" aria-hidden="true">
		<div class="modal-dialog" aria-labelledby="myModalLabel" aria-hidden="true">
			<div class="modal-content">
				<div class="modal-header">
					<legend> 
						<img style="max-width:75px; margin-top: -7px;"src="/static/css/aww/logo.png">&nbsp;&nbsp;&nbsp;Sign up!
					</legend>
				</div>
				<div id="entry_fields" class="modal-body">
					<form id="regForm" class="form" role="form" method="POST">
						<input id="newEmail" class="form-control" name="email" placeholder="Your Email" type="email" />
						<input id="reNewEmail" class="form-control" name="reenteremail" placeholder="Re-enter Email" type="email" />
						<input id="newPass" class="form-control" name="password" placeholder="New Password" type="password" />
						<input id="reNewPass" class="form-control" name="reenterpassword" placeholder="Re-enter Password" type="password" />

						<button class="btn btn-lg btn-primary btn-block" onclick="register(event)" type="submit">Sign up</button>	
					</form>
				</div>
			</div>
		</div>
	</div>
	
	
    <!-- Page Content -->
    <div class="container">
		
        <!-- Portfolio Item Heading -->
        <div class="row">
            <div class="col-lg-12">
				<br/><br/>
				<form id="search" class="navbar-form navbar-right" role="form">
					<strong>Search for profiles:</strong>
					<input id="name" class="form-control" name="name" placeholder="Enter Profile Name" type="text" />
					<button type="submit" onclick="search(event)" class="btn btn-primary">Search</button>
				</form>
                <h1 class="page-header">
                    {{user if nickname is None else nickname}} <small>Hall of fame points: {{len(walloffame_picids or [])}}</small>
                </h1>	
            </div>	
        </div>
        <!-- /.row -->
	<div id="profModal" class="modal fade" role="dialog" tabindex="-1" aria-labelledby="myModalLabel" aria-hidden="true">
		<div class="modal-dialog" aria-labelledby="myModalLabel" aria-hidden="true">
			<div class="modal-content">
				<div class="modal-header">
					<legend> 
						<img style="max-width:75px; margin-top: -7px;"src="/static/css/aww/logo.png">&nbsp;&nbsp;&nbsp;Edit Profile
					</legend>
				</div>
				<div id="updateDiv" class="modal-body">
					<form id="uploader" enctype="multipart/form-data">
						<input id="nickname" class="form-control" name="nickname" placeholder="User name" type="user" value="{{nickname or ""}}" /><br>
						<input id="description" class="form-control" name="description" placeholder="Description" type="description" value="{{description or ""}}" /><br>
						<div style="position:relative;">
						<a class='btn btn-primary' href='javascript:;'>
						Choose File...
						<input name="upload" id="input-1" type="file" class="btn-file" style='position:absolute;z-index:2;top:0;left:0;filter: alpha(opacity=0);-ms-filter:"progid:DXImageTransform.Microsoft.Alpha(Opacity=0)";opacity:0;background-color:transparent;color:transparent;' name="file_source" size="40"  onchange='$("#upload-file-info").html($(this).val());'>
						</a>
						&nbsp;
						<span class='label label-info' id="upload-file-info"></span>
						</div><br>
						<div id="proBar"  hidden class="progress">
							<div id="proBar2" class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
						</div>
						<button class="btn btn-lg btn-primary btn-block" onclick="updateProf(event)" type="submit">Update</button>	
					</form>
				</div>
			</div>
		</div>
	</div>
        <!-- Portfolio Item Row -->
        <div class="row">
            <div class="col-sm-3">
			<div>
                <img id="profilePic" class="img-responsive" src="/pic/profile/{{user}}" alt="">
				<span id="labelSpan" class="label label-default rank-label">Points: {{len(walloffame_picids or [])}}</span>
			</div>
				% if email is not None and email == user:
				<button type="button" class="btn btn-primary" data-toggle="modal" href="#profModal" data-backdrop="true" style="margin-top:5px">Edit profile</button>
				% end
            </div>

            <div class="col-md-4">
                <h3>Description:</h3>
				<p>{{description}}</p>
            </div>

        </div>
        <!-- /.row -->
        <!-- Related Projects Row -->
        <div class="row">

            <div class="col-lg-12">
                <h3 class="page-header">Last 4 to make it to hall of fame</h3>
            </div>
			
			% for picid in sorted(pics, key=lambda key: -pics[key]["time_added"])[:4]: # TODO: move to controller
			% 	pic = pics[picid]
			
			<!-- lightbox modal -->
			<div id="lightboxModal{{picid}}" class="modal fade" role="dialog" tabindex="-1" aria-labelledby="myModalLabel" aria-hidden="true" style="max-height=100%; max-width=100%">
				<div class="modal-dialog" aria-labelledby="myModalLabel" aria-hidden="true">
					<div class="modal-content">
						<img class="img-responsive portfolio-item" src="/pic/halloffame/orig/{{picid}}" alt="">
					</div>
				</div>
			</div>
			
			<div class="col-sm-3 col-xs-6">
				<a href="#lightboxModal{{picid}}" data-toggle="modal" data-backdrop="true">
                     <img class="img-responsive portfolio-item" src="/pic/halloffame/thumb/{{picid}}" alt="">
                </a>
            </div>
			% end

        </div>
        <!-- /.row -->

        <hr>

        <!-- Footer -->
        <footer>
            <div class="row">
                <div class="col-lg-12">
                    <p>Copyright &copy; Cuddles inc. 2015</p>
                </div>
            </div>
            <!-- /.row -->
        </footer>

    </div>
    <!-- /.container -->

    <!-- jQuery -->
    <script src="/static/js/jquery.js"></script>

    <!-- Bootstrap Core JavaScript -->
    <script src="/static/js/bootstrap.min.js"></script>

</body>

</html>
