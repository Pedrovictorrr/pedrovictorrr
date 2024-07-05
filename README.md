## Git Stats

 
<div align="center">
 
 ![image](https://github.com/Pedrovictorrr/pedrovictorrr/assets/82172897/b7e2d638-39fa-4bbe-aeea-971ae46748e2)

  <a href="https://github.com/pedrovictorrr">

 ![](https://github-readme-streak-stats.herokuapp.com/?user=pedrovictorrr&theme=dark&hide_border=false) 
  
 
</div>

<div align="center">
 

</div>
</div>

```php

<?php

use App\Models\User;
use App\Eloquenta\Develop;

class Perfil extends Develop
{
    public function Pedro()
    {
        try {
            $user = User::where('name', 'Pedro Victor Fernandes de Abreu')->first();
            $label = "Laravel Developer";
            if ($user) {
                $skills = [
                    "primarySkillset" => "PHP(LARAVEL)",
                    "front" => [
                        "TypeScript",
                        "JavaScript",
                        "React Native",
                        "React",
                        "Angular",
                        "Vue",
                        "JQuery",
                        "Bootstrap",
                        "Tailwind",
                        "Livewire",
                    ],
                    "back" => [
                        "PHP",
                        "Laravel",
                        "Python",
                        "Django",
                        "C",
                        "Java"
                    ],
                    "devOps" => [
                        "Docker",
                        "AWS",
                        "Ubuntu-server"
                    ],
                    "design" => [
                        "Figma",
                        "Adobe XD"
                    ],
                    "operatingSystems" => [
                        "Linux" => [
                            "Ubuntu",
                            "Debian",
                            "Mint"
                        ],
                        "Windows",
                        "MAC OS X",
                    ],
                ];
                // Vincular as habilidades do usuário
                $user->skills()->sync($skills);
                return "Habilidades atualizadas com sucesso para: $user->name, Cargo $label";
            } else {
                return "Usuário não encontrado.";
            }
        } catch (\Exception $e) {
            return $e->getMessage();
        }
    }
}

?>
```
</div>
