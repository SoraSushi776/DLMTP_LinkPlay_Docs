$docsDir = "C:\Users\Sushi\Documents\Projects\DLMTP_LinkPlay_Docs"

$sections = @(
    @{id="overview";       title="1. 概述";           file="index.md"},
    @{id="file-structure"; title="2. 文件结构";       file="getting-started.md"},
    @{id="enums";          title="3. 枚举与常量";     file="enums.md"},
    @{id="rpc-attribute";  title="4. RPC 属性";       file="rpc-attribute.md"},
    @{id="data-models";    title="5. 数据模型";       file="data-models.md"},
    @{id="client";         title="6. 核心客户端 API"; file="client.md"},
    @{id="message-handler";title="7. 消息处理器";     file="message-handler.md"},
    @{id="protocol";       title="8. 协议格式";       file="protocol.md"},
    @{id="examples";       title="9. 完整使用示例";   file="examples.md"},
    @{id="faq";            title="10. 常见问题";      file="faq.md"}
)

function Strip-Frontmatter($text) {
    if ($text.StartsWith("---")) {
        $idx = $text.IndexOf("---", 3)
        if ($idx -gt 0) {
            return $text.Substring($idx + 3).Trim()
        }
    }
    return $text.Trim()
}

function Convert-MdToHtml($text) {
    $lines = $text -split "`n"
    $out = @()
    $i = 0
    while ($i -lt $lines.Count) {
        $line = $lines[$i]
        # Skip YAML frontmatter separator lines
        if ($line -eq "---") { $i++; continue }
        # Code blocks
        if ($line -match '^```') {
            $i++
            $codeLines = @()
            while ($i -lt $lines.Count -and $lines[$i] -notmatch '^```') {
                $codeLines += $lines[$i]
                $i++
            }
            $i++
            $code = [System.Web.HttpUtility]::HtmlEncode(($codeLines -join "`n"))
            $out += "<pre><code>$code</code></pre>"
            continue
        }
        # Tables
        if ($line -match '^\|.*\|.*\|$') {
            $tableLines = @($line)
            $i++
            if ($i -lt $lines.Count -and $lines[$i] -match '^\|[\s\-:|]+\|$') {
                $i++
                while ($i -lt $lines.Count -and $lines[$i] -match '^\|.*\|.*\|$') {
                    $tableLines += $lines[$i]
                    $i++
                }
                $out += (Render-Table $tableLines)
                continue
            }
        }
        # Headings
        if ($line -match '^# (.+)') { $out += "<h1>" + (Inline-Md $Matches[1]) + "</h1>"; $i++; continue }
        if ($line -match '^## (.+)') { $out += "<h2>" + (Inline-Md $Matches[1]) + "</h2>"; $i++; continue }
        if ($line -match '^### (.+)') { $out += "<h3>" + (Inline-Md $Matches[1]) + "</h3>"; $i++; continue }
        if ($line -match '^#### (.+)') { $out += "<h4>" + (Inline-Md $Matches[1]) + "</h4>"; $i++; continue }
        # Blockquote
        if ($line -match '^> (.+)') { $out += "<blockquote><p>" + (Inline-Md $Matches[1]) + "</p></blockquote>"; $i++; continue }
        # List items
        if ($line -match '^[\-\*]\s+(.+)') { $out += "<li>" + (Inline-Md $Matches[1]) + "</li>"; $i++; continue }
        # Horizontal rule
        if ($line -eq '---' -or $line -eq '***') { $out += "<hr>"; $i++; continue }
        # Empty line
        if ($line.Trim() -eq '') { $i++; continue }
        # Paragraph
        if ($line.Trim() -ne '') {
            $prevMatch = $line -match '\[←|→'
            if (-not $prevMatch) {
                $out += "<p>" + (Inline-Md $line) + "</p>"
            }
        }
        $i++
    }
    return $out -join "`n"
}

function Inline-Md($text) {
    $t = $text
    $t = $t -replace '\*\*(.+?)\*\*', '<strong>$1</strong>'
    $t = $t -replace '`([^`]+)`', '<code>$1</code>'
    $t = $t -replace '\[([^\]]+)\]\(([^)]+)\)', '<a href="$2">$1</a>'
    return $t
}

function Render-Table($lines) {
    $header = $lines[0].Trim("|").Split("|") | ForEach-Object { (Inline-Md $_.Trim()) }
    $html = @("<table><thead><tr>")
    foreach ($h in $header) { $html += "<th>$h</th>" }
    $html += "</tr></thead><tbody>"
    for ($r = 1; $r -lt $lines.Count; $r++) {
        $cells = $lines[$r].Trim("|").Split("|") | ForEach-Object { (Inline-Md $_.Trim()) }
        $html += "<tr>"
        foreach ($c in $cells) { $html += "<td>$c</td>" }
        $html += "</tr>"
    }
    $html += "</tbody></table>"
    return $html -join "`n"
}

function Escape-Html($text) {
    return [System.Web.HttpUtility]::HtmlEncode($text)
}

# Build sidebar
$sidebarItems = @()
$first = $true
foreach ($s in $sections) {
    $active = if ($first) { ' class="active"' } else { '' }
    $sidebarItems += "            <li><a href=`"#$($s.id)`"$active>$($s.title)</a></li>"
    $first = $false
}

# Build content
$contentParts = @()
foreach ($s in $sections) {
    $filePath = Join-Path $docsDir $s.file
    $mdText = Get-Content $filePath -Raw -Encoding UTF8
    $mdText = Strip-Frontmatter $mdText
    $htmlBody = Convert-MdToHtml $mdText
    $tag = ''
    if ($s.id -eq 'overview') {
        $tag = "<span class=`"tag`">命名空间: DLMTP_LinkPlay</span>`n"
    }
    $contentParts += @"
        <!-- $($s.title) -->
        <div class="section" id="$($s.id)">
$tag$htmlBody
        </div>
"@
}

$css = @'
<style>
:root {
    --sidebar-width: 260px; --bg: #fafbfc; --sidebar-bg: #1b1f2a;
    --sidebar-text: #c8ccd4; --sidebar-hover: #2d3344; --sidebar-active: #3b82f6;
    --text: #1f2937; --text-light: #6b7280; --border: #e5e7eb;
    --code-bg: #f3f4f6; --code-text: #dc2626; --link: #3b82f6;
    --table-stripe: #f9fafb; --heading: #111827;
    --blockquote-bg: #eff6ff; --blockquote-border: #3b82f6;
}
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",Roboto,sans-serif;line-height:1.7;color:var(--text);background:var(--bg);display:flex;min-height:100vh;}
.sidebar{position:fixed;top:0;left:0;width:var(--sidebar-width);height:100vh;background:var(--sidebar-bg);color:var(--sidebar-text);overflow-y:auto;z-index:100;display:flex;flex-direction:column;}
.sidebar-header{padding:24px 20px 16px;border-bottom:1px solid rgba(255,255,255,0.08);font-size:15px;font-weight:600;color:#f1f5f9;}
.sidebar-header small{display:block;font-weight:400;font-size:12px;color:#94a3b8;margin-top:4px;}
.sidebar-nav{flex:1;padding:8px 0;list-style:none;}
.sidebar-nav li a{display:block;padding:8px 20px;color:var(--sidebar-text);text-decoration:none;font-size:13.5px;border-left:3px solid transparent;transition:all 0.15s;}
.sidebar-nav li a:hover{background:var(--sidebar-hover);color:#f1f5f9;}
.sidebar-nav li a.active{background:rgba(59,130,246,0.15);color:#60a5fa;border-left-color:var(--sidebar-active);}
.sidebar-footer{padding:12px 20px;border-top:1px solid rgba(255,255,255,0.08);font-size:12px;color:#64748b;}
.main{margin-left:var(--sidebar-width);flex:1;min-width:0;}
.content{max-width:860px;margin:0 auto;padding:48px 40px 40px;width:100%;}
h1{font-size:28px;font-weight:700;color:var(--heading);margin-bottom:4px;}
h2{font-size:20px;font-weight:600;color:var(--heading);margin-top:40px;margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid var(--border);}
h3{font-size:16px;font-weight:600;color:var(--heading);margin-top:28px;margin-bottom:10px;}
h4{font-size:14px;font-weight:600;color:var(--heading);margin-top:20px;margin-bottom:8px;}
p{margin-bottom:12px;font-size:15px;}
a{color:var(--link);text-decoration:none;}
a:hover{text-decoration:underline;}
code{background:var(--code-bg);padding:2px 6px;border-radius:4px;font-family:"JetBrains Mono",Consolas,monospace;font-size:13px;color:var(--code-text);}
pre{background:#1e293b;color:#e2e8f0;padding:18px 20px;border-radius:8px;overflow-x:auto;margin:14px 0;font-size:13px;line-height:1.6;}
pre code{background:none;color:inherit;padding:0;font-size:inherit;}
table{width:100%;border-collapse:collapse;margin:14px 0 20px;font-size:14px;}
th,td{border:1px solid var(--border);padding:10px 14px;text-align:left;}
th{background:#f8fafc;font-weight:600;color:#374151;font-size:13px;}
tr:nth-child(even) td{background:var(--table-stripe);}
blockquote{background:var(--blockquote-bg);border-left:4px solid var(--blockquote-border);padding:12px 18px;margin:14px 0;border-radius:0 6px 6px 0;color:#374151;font-size:14px;}
blockquote p{margin:0;}
hr{border:none;border-top:1px solid var(--border);margin:28px 0;}
.section{scroll-margin-top:30px;}
.tag{display:inline-block;background:#e0e7ff;color:#3730a3;padding:2px 8px;border-radius:4px;font-size:12px;font-weight:500;margin-bottom:10px;}
ul,ol{margin:10px 0 14px 24px;font-size:15px;}
li{margin-bottom:4px;}
.site-footer{margin-top:48px;padding:20px 0;border-top:1px solid var(--border);text-align:center;font-size:13px;color:var(--text-light);}
.site-footer a{color:var(--link);font-weight:500;}
.sidebar::-webkit-scrollbar{width:5px;}
.sidebar::-webkit-scrollbar-track{background:transparent;}
.sidebar::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.1);border-radius:3px;}
@media(max-width:768px){.sidebar{width:220px;}.main{margin-left:220px;}.content{padding:24px 20px;}}
</style>
'@

$js = @'
<script>
document.addEventListener("DOMContentLoaded",function(){
    var links=document.querySelectorAll(".sidebar-nav a");
    var sections=document.querySelectorAll(".section");
    var observer=new IntersectionObserver(function(entries){
        entries.forEach(function(entry){
            if(entry.isIntersecting){
                links.forEach(function(a){a.classList.remove("active")});
                var id=entry.target.id;
                var active=document.querySelector('.sidebar-nav a[href="#'+id+'"]');
                if(active)active.classList.add("active");
            }
        });
    },{rootMargin:"-40px 0px -60% 0px"});
    sections.forEach(function(s){observer.observe(s)});
    links.forEach(function(a){
        a.addEventListener("click",function(e){
            e.preventDefault();
            var target=document.querySelector(this.getAttribute("href"));
            if(target)target.scrollIntoView({behavior:"smooth"});
        });
    });
});
</script>
'@

$html = @"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>DLMTP_LinkPlay SDK 文档</title>
$css
</head>
<body>
<aside class="sidebar">
    <div class="sidebar-header">DLMTP_LinkPlay SDK<small>Unity 联机客户端文档 · v2.0</small></div>
    <ul class="sidebar-nav">
$($sidebarItems -join "`n")
    </ul>
    <div class="sidebar-footer"><a href="https://github.com/your-repo/DLMTP_LinkPlay" target="_blank">GitHub →</a></div>
</aside>
<div class="main"><div class="content">
$($contentParts -join "`n`n")
<div class="site-footer">
    <a href="https://github.com/your-repo/DLMTP_LinkPlay" target="_blank">View on GitHub</a>
    · <a href="https://github.com/your-repo/DLMTP_LinkPlay/issues" target="_blank">问题反馈</a>
    · 文档版本 v2.0 · 最后更新 2026-05-17
</div>
</div></div>
$js
</body>
</html>
"@

$outputPath = Join-Path $docsDir "index.html"
$html | Out-File -FilePath $outputPath -Encoding UTF8
Write-Host "Generated: $outputPath"
Write-Host "Size: $($html.Length) chars"
