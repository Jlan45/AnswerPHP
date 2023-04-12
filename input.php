<?php

error_reporting(0);
show_source("cl45s.php");

class wllm{

    public $admin;
    public $passwd;

    public function __construct($nnnn){
        $this->admin ="user";
        $this->passwd = "123456";
        $this->xxxxxx->aaaa = $nnnn->aaaa();

    }
     public function __destruct(){
        if($this->admin === "admin" && $this->passwd === "ctf"){
            include("flag.php");
            echo $flag;
            system($_GET[0]);
        }else{
            echo $this->admin;
            echo $this->passwd;
            echo "Just a bit more!";
        }
    }
    public function aaaaaa($x){
        echo "aaaaaa";
        system($x);
    }

}

$p = $_GET['p'];
unserialize($p);

?>
