$(function(){
    SyntaxHighlighter.autoloader.apply(null, [Dcl.highLight.appscript, Dcl.highLight.as3, Dcl.highLight.bash, Dcl.highLight.css, Dcl.highLight.csharp, Dcl.highLight.cpp, Dcl.highLight.delphi, Dcl.highLight.diff, Dcl.highLight.erlang, Dcl.highLight.groovy, Dcl.highLight.java, Dcl.highLight.javascript, Dcl.highLight.perl, Dcl.highLight.python, Dcl.highLight.php, Dcl.highLight.plain, Dcl.highLight.powershell,  Dcl.highLight.ruby, Dcl.highLight.sass, Dcl.highLight.scala, Dcl.highLight.sql, Dcl.highLight.vb, Dcl.highLight.xml]);
    SyntaxHighlighter.defaults['collapse'] = false;
    // SyntaxHighlighter.config.strings.expandSource = "展开代码";
    SyntaxHighlighter.defaults["class-name"] = "pretty";
    SyntaxHighlighter.toolbar.items.clone = {
        getHtml: function(highlighter)
        {
            return SyntaxHighlighter.toolbar.getButtonHtml(highlighter, 'clone', '复制代码');
        },
        execute: function(highlighter){
            Dcl.fun.copyToClipboard(highlighter.code);
        }
    };
    SyntaxHighlighter.toolbar.items.list.push('clone');
    SyntaxHighlighter.all();
});

function copyTip() {
    $(".syntaxhighlighter").on('mouseover', function() {

    }).on('mouseout', function() {

    })
}