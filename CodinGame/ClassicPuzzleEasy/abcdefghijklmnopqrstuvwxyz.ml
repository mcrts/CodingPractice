(* Auto-generated code below aims at helping you parse *)
(* the standard input according to the problem statement. *)
open Printf

let next_char c = Char.chr (Char.code c + 1)
;;

type symbol = {
    c: char;
    pos: int * int;
}
let symbol_print s = 
    let x, y = s.pos in
    let msg = sprintf "symbol<c=%c, (x=%d, y=%d)>" s.c x y in
    prerr_endline msg
;;


type array2D = {
    n : int;
    m : int;
    array : string;
}
let array2D_print arr = 
    let msg = sprintf "%d %d" arr.n arr.m in
    prerr_endline msg;

    for i = 0 to arr.n - 1 do
        prerr_endline (String.sub arr.array (i * arr.m) arr.m);
    done;
;;
let array2D_send_solution arr = 
    for i = 0 to arr.n - 1 do
        print_endline (String.sub arr.array (i * arr.m) arr.m);
    done;
;;
let array2D_build n m arr = {
    n = n;
    m = m;
    array = arr;
};;
let array2D_addline arr line = 
    {
        n = arr.n + 1;
        m = String.length line;
        array = arr.array ^ line;
    }
let array2D_get arr i =
    let x, y = i in
    {
        c = String.get arr.array (y*arr.m + x);
        pos = (x, y);
    }
;;
let array2D_start arr =
    let i = String.index arr.array 'a' in
    {
        c = 'a';
        pos = ((i mod arr.m), (i / arr.m));
    }
;;
let array2D_starts arr =
    let l0 = List.mapi (fun i c -> {
        c = c;
        pos = ((i mod arr.m), (i / arr.m));
    }) (arr.array |> String.to_seq |> List.of_seq) in
    List.filter (fun sy -> Char.equal sy.c 'a') l0
;;
let array2D_index_is_in arr i =
    let x, y = i in
    if ((0 <= x) && (x < arr.m) && (0 <= y) && (y < arr.n)) then
        true
    else
        false
;;
let array2D_neighbours arr s =
    let x, y = s.pos in
    let l0 = [(x - 1, y); (x + 1, y); (x, y - 1); (x, y + 1)] in
    let l1 = List.filter (array2D_index_is_in arr) l0 in
    let l2 = List.map (array2D_get arr) l1 in
    List.filter (fun sy -> Char.equal sy.c (next_char s.c)) l2
;;
let rec array2D_path arr acc s =
    let next_acc = s::acc in
    match s.c with
    | 'z' -> next_acc
    | _ -> match array2D_neighbours arr s with
        | x::xs -> array2D_path arr next_acc x
        | _ -> next_acc
;;

let array2D_solve arr =
    let starts = (array2D_starts arr) in
    let paths = List.map (array2D_path arr []) starts in
    List.find (fun p -> 26 = List.length p) paths
;;

let array2D_encode arr path = 
    let f i c =
        let pos = ((i mod arr.m), (i / arr.m)) in
        let s = array2D_get arr pos in
        if (List.mem s path) then s.c else '-'
    in
    {
        n = arr.n;
        m = arr.m;
        array = String.mapi f arr.array;
    }
;;
let parse =
    let n = int_of_string (input_line stdin) in
    let arr = ref (array2D_build 0 0 "") in
    for i = 0 to n - 1 do
        let line = input_line stdin in
        arr := array2D_addline (arr.contents) line;
    done;
    arr.contents
;;
    

let main = 
    let arr = parse in
    array2D_print arr;
    let p = array2D_solve arr in
    let s = array2D_encode arr p in
    array2D_send_solution s;
;;


(* Write an answer using print_endline *)
(* To debug: prerr_endline "Debug message"; *)
main ;;