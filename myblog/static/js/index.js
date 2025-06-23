        console.log(screen.width);

        window.onload = styleInit;

        window.addEventListener('pageshow', function(event) {
        if (event.persisted) {
            window.location.reload()
        }
        });

        function styleInit(){

            listStyleInit();
            let btn = document.getElementById("btn-submit");
            btn.onmouseover = () => btn.className =  "btn-submit-over";
            btn.onmouseout = () => btn.className =  "btn-submit";
            btn.onclick = changeSubmit;
        }

        function listStyleInit() {
            let options = document.getElementsByClassName('options');

                console.log(options.length);

                for(let j=0; j<options.length; j++) {
            
                options[j].style.width = "250px";
                options[j].style.height = "50px";
                options[j].style.fontSize = "x-large";
                options[j].style.backgroundColor = "#f4c1c1";
            
            }
        }

        function changeSubmit() {
            let e1 = document.getElementById("vege");
            let text1 = e1.options[e1.selectedIndex].text;
            let e2 = document.getElementById("meat");
            let text2 = e2.options[e2.selectedIndex].text;

            if( (text1 === '不吃菜') && (text2 === '不吃肉'))
                alert('菜類跟肉類至少挑一項!');
            else
            {
                document.ingredients.btn_submit.value = '出菜中.';
                document.getElementById("ingredients").submit();
                ai_prog = document.getElementById("ai-prog");
                ai_prog.hidden = false;
                move();
            }
        }


        let i = 0;
        function move() {
        if (i == 0) {
        i = 1;
          let elem = document.getElementById("ai-prog-bar");
          let width = 1;
          let interval = 0;
          let round = 0;
          let id = setInterval(frame, 10);
          function frame() {
            width++;
            interval++;

            if(((interval)%100) == 0) {
              round = round%3;
              round++;
          }

          switch(round)
          {
              case 1:
              document.ingredients.btn_submit.value = '出菜中.';
              break;
              case 2:
              document.ingredients.btn_submit.value = '出菜中..';
              break;
              case 3:
              document.ingredients.btn_submit.value = '出菜中...';
              break;
          }

          if(width > 100)
              width = 0;

            elem.style.width = width + "%";
        }
      }
    }