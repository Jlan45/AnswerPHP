?> <?php 
include("./xxxiscc.php"); 
class boy { 
    public $like; 
    public function __destruct() { 
        echo "能请你喝杯奶茶吗？<br>"; 
        @$this->like->make_friends(); 
    } 
    public function __toString() { 
        echo "拱火大法好<br>"; 
        return $this->like->string; 
    } 
} 

class girl { 
    private $boyname; 
    public function __call($func, $args) { 
        echo "我害羞羞<br>"; 
        isset($this->boyname->name);   
    } 
} 

class helper { 
    private $name; 
    private $string; 
    public function __construct($string) { 
        $this->string = $string; 
    } 
    public function __isset($val) { 
        echo "僚机上线<br>"; 
        echo $this->name; 
    } 
    public function __get($name) { 
        echo "僚机不懈努力<br>"; 
        $var = $this->$name; 
        $var[$name](); 
    } 
} 
class love_story { 
    public function love() { 
        echo "爱情萌芽<br>"; 
        array_walk($this, function($make, $colo){ 
            echo "坠入爱河，给你爱的密码<br>"; 
            if ($make[0] === "girl_and_boy" && $colo === "fall_in_love") { 
                global $flag; 
                echo $flag; 
            } 
        }); 
    } 
} 

if (isset($_GET["iscc"])) { 
    $a=unserialize($_GET['iscc']); 
} else { 
    highlight_file(__FILE__); 
}