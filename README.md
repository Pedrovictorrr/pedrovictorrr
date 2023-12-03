

## Sobre 👋

</div>
...

```php
<?php
class Perfil extends Develop {
     
      public function Pedro()
      {
          try {
      
              $user = User::where('name', 'Pedro Victor Fernandes de Abreu')->first();
              $label = "Laravel Developer";
              $level = "Mid Level";
      
              if ($user) {
                  $skills = [
                      "primarySkillset" => "PHP(LARAVEL)",
                      "front" => [
                          "TypeScript", "JavaScript", "React Native",
                          "React", "Angular", "Vue", "JQuery",
                          "Bootstrap", "Tailwind", "Livewire"
                      ],
                      "back" => [
                          "PHP", "Laravel", "Python", "Django", "C"
                      ],
                      "devOps" => [
                          "Docker", "AWS"
                      ],
                      "design" => [
                          "Figma"
                      ],
                      "operatingSystems" => [
                          "Linux", "Ubuntu", "Debian", "Windows", "MAC OS X"
                      ],
                  ];
      
                  // Vincular as habilidades do usuário
                  $user->skills()->sync($skills);
      
                  return "Habilidades atualizadas com sucesso para Pedro Victor Fernandes de Abreu. Label: $label, Level: $level";
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

<div align="center">
 



 ## Stacks

<div  align="center" style="display: inline_block;   display: flex; justify-content: center;"><br>
  <img align="center" alt="Pedro-PHP" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/php/php-original.svg">
    <img align="center" alt="Pedro-Laravel" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/laravel/laravel-plain.svg">
  <img align="center" alt="Pedro-Js" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-plain.svg">
  <img  align="center" alt="Pedro-Ts" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" />
  <img align="center" alt="Pedro-Js" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original-wordmark.svg" />
  <img align="center" alt="Pedro-Jquery" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jquery/jquery-original.svg" />
   <img align="center" alt="Pedro-C" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/ubuntu/ubuntu-plain.svg" />
   <img align="center" alt="Pedro-C" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vuejs/vuejs-original.svg" />
   <img align="center" alt="Pedro-C" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/figma/figma-original.svg" />
   <img align="center" alt="Pedro-C" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/amazonwebservices/amazonwebservices-original.svg" /><br>
  <img align="center" alt="Pedro-Js" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/angularjs/angularjs-plain.svg">
  <img align="center" alt="Pedro-HTML" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original.svg">
   <img align="center" alt="Pedro-CSS" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original.svg">
  <img align="center" alt="Pedro-bootstrap" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original-wordmark.svg" />
<img align="center" alt="Pedro-tailwind" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-plain.svg" />
<img  align="center" alt="Pedro-mysql" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg" />
  <img align="center" alt="Pedro-Docker" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original-wordmark.svg" />
  <img align="center" alt="Pedro-Python" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">
      <img align="center" alt="Pedro-Django" height="30" width="40" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg" />
  <img align="center" alt="Pedro-C" height="30" width="40" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/c/c-original.svg">

</div>

## Git Stats
 
<div align="center">
  <a href="https://github.com/pedrovictorrr">

 ![](https://github-readme-streak-stats.herokuapp.com/?user=pedrovictorrr&theme=dark&hide_border=false) 
  
 
</div>

<div align="center">
 

## Meus Projetos

| Sistema de Plano médico | Reserva de mesa | Sistema de estoque |
|:---:|:---:|:---:|
| ![image](https://github.com/Pedrovictorrr/pedrovictorrr/assets/82172897/c4eabbcf-cf32-4519-b150-66c7c7d8544c) | ![image](https://github.com/Pedrovictorrr/pedrovictorrr/assets/82172897/a0eef92f-c0ac-42ee-88dd-5aa781fadf30) | ![image](https://github.com/Pedrovictorrr/pedrovictorrr/assets/82172897/fc73cb0a-f34e-4a3e-9f62-6432acd31e93)
 |

| Lanche na praia | Stock Sneakers | DETRO |
|:---:|:---:|:---:|
|![Captura de tela de 2023-07-31 23-38-16](https://github.com/Pedrovictorrr/pedrovictorrr/assets/82172897/f8cc500f-1842-4022-baab-bee41f501b46) |![127 0 0 1_8000_login (1)](https://github.com/Pedrovictorrr/pedrovictorrr/assets/82172897/5db45516-138a-4d2a-ac7b-ea6f23cf1947) |![image](https://github.com/Pedrovictorrr/pedrovictorrr/assets/82172897/6d686673-4855-4ffb-88c0-b59803e9f730)|

## Status

<br>
<div style="padding:20px;">
 
 [![Ashutosh's github activity graph](https://github-readme-activity-graph.vercel.app/graph?username=pedrovictorrr&theme=github-compact)](https://github.com/ashutosh00710/github-readme-activity-graph)
</div>

[website]: https://pedro-abreu.onrender.com/
[linkedin]: https://www.linkedin.com/in/pedro-victor-fernandes-de-abreu-98411816a/

<br>

## Rede sociais

🏡 [Website][website] **|**
👔 [LinkedIn][linkedin]


</div>
