<?php
session_start();
require('koneksi.php');

$error = '';

if (isset($_SESSION['username'])) {
    header("Location: index.php");
    exit;
}

if (isset($_POST['submit'])) {

    $username = mysqli_real_escape_string($con, trim($_POST['username']));
    $password = mysqli_real_escape_string($con, trim($_POST['password']));

    if (!empty($username) && !empty($password)) {

        $query  = "SELECT * FROM users WHERE username = '$username'";
        $result = mysqli_query($con, $query);

        if (mysqli_num_rows($result) > 0) {

            $user = mysqli_fetch_assoc($result);
            $hash = $user['password'];

            if (password_verify($password, $hash)) {
                $_SESSION['username'] = $username;
                header("Location: index.php");
                exit;   // <<< PENTING
            } else {
                $error = "Password salah!";
            }

        } else {
            $error = "Username tidak terdaftar!";
        }

    } else {
        $error = "Username dan password wajib diisi!";
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Login</title>
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
<link rel="stylesheet" href="style.css">
</head>

<body>
<section class="container-fluid mb-4">
    <section class="row justify-content-center">
        <section class="col-12 col-sm-6 col-md-4">
            <form class="form-container" action="login.php" method="POST">
                <h4 class="text-center font-weight-bold">Sign-In</h4>

                <?php if($error != ''){ ?>
                    <div class="alert alert-danger"><?= $error; ?></div>
                <?php } ?>

                <div class="form-group">
                    <label>Username</label>
                    <input type="text" class="form-control" name="username" placeholder="Masukkan username">
                </div>

                <div class="form-group">
                    <label>Password</label>
                    <input type="password" class="form-control" name="password" placeholder="Password">
                </div>

                <button type="submit" name="submit" class="btn btn-primary btn-block">Sign In</button>

                <div class="form-footer mt-2">
                    <p>Belum punya account? <a href="register.php">Register</a></p>
                </div>
            </form>
        </section>
    </section>
</section>
</body>
</html>
