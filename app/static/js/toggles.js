
function toggle_open(event){
    event.target.data_target.classList.remove('close');
    event.target.data_target.classList.add('open');
}

function toggle_close(event){
    event.target.data_target.classList.remove('open');
    event.target.data_target.classList.add('close');
}

function toggle_close_all(event){
    document.querySelectorAll(".open").forEach(f => {
        f.classList.remove('open');
        f.classList.add('close');
    })
    
}

function toggle_init(item){
    item.data_target = document.querySelector(item.getAttribute("data-target"));
}

function init_data_state(elem){
    var state = elem.getAttribute("data-state");
    state = JSON.parse(state);
    elem.data_state = state
    if (state){
        for( item in state){
            for(value in state[item]){
                for(cond in state[item][value]){
                    var string = item+"."+value+state[item][value][cond];
                    console.log(eval(item+"."+value + state[item][value][cond]))
                    if(eval(string))
                        elem.classList.add(cond)
                    console.log(item+" -> "+value+" "+state[item][value][cond]+" : "+cond);
                }
            }
        }
    }
}

document.querySelectorAll(".toggel").forEach(toggle_init)
document.querySelectorAll(".toggel[data-action]").forEach(f => {f.addEventListener("click", window["toggle_"+f.getAttribute('data-action')])})
document.querySelectorAll("[data-state]").forEach(f => init_data_state(f))
