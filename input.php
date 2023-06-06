<?php
highlight_file(__FILE__);
error_reporting(0);

class AAA
{
    private $cmd;

    public function __destruct()
    {
        echo "This is cmd :" . $this->cmd;
    }

    public function __invoke()
    {
        system($this->cmd, $ret,$a[0],$a['ssss']->bbb,$a->aaa());
    }
}

class BBB
{
    protected $name;

    public function __toString()
    {
        return $this->name->obj;
    }
}

class EEE
{
    public $var;

    public function __get($var)
    {
        $this->var();
    }
}

unserialize($_POST['pop']);
?>
