#load @".paket\load\HtmlAgilityPack.fsx"
open System.Net
open System
open HtmlAgilityPack
open System.Net
open System.IO
open System.Text.RegularExpressions

let jupyterCellTemplate = "
    {
    \"cell_type\": \"code\",
    \"execution_count\": 1,
    \"metadata\": {},
    \"outputs\": [],
    \"source\": [
        ##content##
    ]
    }"
    
let jupyterTemplate = File.ReadAllText "jupyter.template"
let py2jupy (path:string) =     
    let cells = 
        Regex.Split(File.ReadAllText path, "\r\n\r\n")
        |> Array.map (fun str -> str.Split('\n') |> Array.map (fun line -> sprintf "\"%s\\n\"" <| line.TrimEnd().Replace("\"","\\\"")) |> Array.reduce (sprintf "%s,\n%s"))
        |> Array.map (fun str -> jupyterCellTemplate.Replace("##content##", str))
        |> Array.reduce (sprintf "%s,\n%s")
    
    let text = jupyterTemplate.Replace("##cells##", cells)
    File.WriteAllText(path.Replace(".py",".ipynb"), text)

//py2jupy @"data\Classification with Decision Trees\decision_tree.py"

let web = HtmlWeb()
let main = web.Load("https://thdiaman.github.io/deeplearning/modules/tutorial/introduction/")
let convertA (a: HtmlNode) = a.InnerText.Trim(), a.Attributes.["href"].Value
let sidebar = main.DocumentNode.SelectSingleNode(".//div[contains(@class,'sidebar')]") 
let pages = 
    sidebar.SelectNodes("//a")
     |> Seq.cast<HtmlNode> 
     |> Seq.map(fun node -> node.InnerText.Trim(), node.Attributes.["href"].Value)
     |> Seq.skipWhile (fun (text,href) -> not <| text.StartsWith("OCR"))

let wc = new WebClient()
wc.Proxy <- null
let dlButSkip404s (url:string) path = 
    try  
        wc.DownloadFile(url, path)  
        true
    with
    | :? System.Net.WebException as ex when ex.Message.Contains("404") -> printfn "%s" ex.Message; false
    | ex -> reraise();false

pages 
|> Seq.map(fun (title,url) -> 
    let page = web.Load(url)
    let links = 
        page
            .DocumentNode
            .SelectNodes("/html/body/div/div[2]/div/div/div//a")
        |> Seq.cast<HtmlNode>
        |> Seq.map convertA
    
    let directoryName = sprintf "%s\\Data\\%s" __SOURCE_DIRECTORY__ title
    if directoryName |> Directory.Exists |> not then Directory.CreateDirectory(directoryName) |> printfn "%A"



    links
    |> Seq.map snd
    |> Seq.map (fun url -> 
            let filename = url.Split('/') |> Array.last
            printfn "%s, %s" url filename
            let path = System.IO.Path.Combine(directoryName,filename)
            if File.Exists path then 
                if path.EndsWith(".py") then py2jupy path
            else 
                match filename.Split('.') |> Array.last with
                | "py" ->
                    if dlButSkip404s url path then py2jupy path
                | "pdf"
                | "zip"
                | "csv"
                | "npz"
                | "h5" -> dlButSkip404s url path |> ignore
                | extension -> printfn "skipping unknown extension %s" extension  )
    |> Array.ofSeq)
|> Array.ofSeq

