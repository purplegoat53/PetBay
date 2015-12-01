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

    <title>PetBay</title>

    <!-- Bootstrap Core CSS -->
    <link href="/static/css/bootstrap.min.css" rel="stylesheet">

    <!-- Custom CSS -->
    <link href="/static/css/thumbnail-gallery.css" rel="stylesheet">
	
	<!-- Magnific Popup core CSS file -->
	<link rel="stylesheet" href="magnific-popup/magnific-popup.css">
	
	<!-- Magnific Popup core JS file -->
	<script src="magnific-popup/jquery.magnific-popup.js"></script>

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
                    <li>
                        <a href="/profile">Profile</a>
                    </li>
                </ul>
				<form id="signout" class="navbar-form navbar-right" role="form">
					Logged in as:&nbsp;{{email}}
					<button type="submit" onclick="showUp(event)" class="btn btn-primary">Upload</button>
					<button type="submit" onclick="logout(event)" class="btn btn-primary">Logout</button>
				</form>
            </div>
            <!-- /.navbar-collapse -->
        </div>
        <!-- /.container -->
    </nav>

    <!-- Page Content -->
    <div class="container">

        <!-- Portfolio Item Heading -->
        <div class="row">
            <div class="col-lg-12">
                <h1 class="page-header">
                    {{email if nickname is None else nickname}} <small>Hall of fame points: {{len(walloffame_picids or [])}}</small>
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
						<input id="nickname" class="form-control" name="nickname" placeholder="User name" type="user" /><br>
						<input id="description" class="form-control" name="description" placeholder="Description" type="description" /><br>
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
                <img class="img-responsive" src="/pic/profile/{{email}}" alt="">
				<button type="button" class="btn btn-primary" data-toggle="modal" href="#profModal" data-backdrop="true" style="margin-top:5px">Edit profile</button>
            </div>

            <div class="col-md-4">
                <h3>Description</h3>
				<p>{{description}}</p>
            </div>

        </div>
        <!-- /.row -->

        <!-- Related Projects Row -->
        <div class="row">

            <div class="col-lg-12">
                <h3 class="page-header">Last 4 to make it to hall of fame</h3>
            </div>

            <div class="col-sm-3 col-xs-6">
                <a href="#">
                    <img class="img-responsive portfolio-item" src="/static/css/aww/cat1.jpg" alt="">
                </a>
            </div>
			
            <div class="col-sm-3 col-xs-6">
                <a href="#">
                    <img class="img-responsive portfolio-item" onclick="test-popup-link" src="http://placehold.it/500x300" alt="">
                </a>
            </div>

            <div class="col-sm-3 col-xs-6">
                <a href="#">
                    <img class="img-responsive portfolio-item" onclick="test-popup-link" src="http://placehold.it/500x300" alt="">
                </a>
            </div>

            <div class="col-sm-3 col-xs-6">
                <a href="#">
                    <img class="img-responsive portfolio-item" src="http://placehold.it/500x300" alt="">
                </a>
            </div>

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
