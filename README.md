## Git Stats
 
<div align="center">
  <a href="https://github.com/pedrovictorrr">

 ![](https://github-readme-streak-stats.herokuapp.com/?user=pedrovictorrr&theme=dark&hide_border=false) 
  
 
</div>

<div align="center">
 

## Meus Projetos

| Lanche na praia | Stock Sneakers | DETRO |
|:---:|:---:|:---:|
|![Captura de tela de 2023-07-31 23-38-16](https://github.com/Pedrovictorrr/pedrovictorrr/assets/82172897/f8cc500f-1842-4022-baab-bee41f501b46) |![127 0 0 1_8000_login (1)](https://github.com/Pedrovictorrr/pedrovictorrr/assets/82172897/5db45516-138a-4d2a-ac7b-ea6f23cf1947) |![image](https://github.com/Pedrovictorrr/pedrovictorrr/assets/82172897/6d686673-4855-4ffb-88c0-b59803e9f730)|

| Sistema de Plano médico | Reserva de mesa | Sistema de estoque |
|:---:|:---:|:---:|
| ![image](https://github.com/Pedrovictorrr/pedrovictorrr/assets/82172897/c4eabbcf-cf32-4519-b150-66c7c7d8544c) | ![image](https://github.com/Pedrovictorrr/pedrovictorrr/assets/82172897/a0eef92f-c0ac-42ee-88dd-5aa781fadf30) | ![image](https://github.com/Pedrovictorrr/pedrovictorrr/assets/82172897/fc73cb0a-f34e-4a3e-9f62-6432acd31e93)
 |


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
