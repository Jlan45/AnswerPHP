<?php
    class A{
        public $target;
        function __construct(){
            $this->target = new B;
        }
        function __destruct(){
            $this->target->action();
        }
    }
    class B{
        function action(){
            echo "action B";
        }
    }
    class C{
        public $test;
        function action(){
            echo "action A";
            eval($this->test);
        }
    }
    unserialize($_GET['test']);
?>