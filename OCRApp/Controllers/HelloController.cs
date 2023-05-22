using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using IronPython.Hosting;

[Route("api/[controller]")]
[ApiController]
public class HelloController : ControllerBase
{
    [HttpGet("{name}")]
    public IActionResult Get(string name)
    {
        var engine = Python.CreateEngine();
        var scope = engine.CreateScope();

        string pythonScriptPath = Path.Combine(Directory.GetCurrentDirectory(), "Scripts", "HelloScript.py");

        engine.ExecuteFile(pythonScriptPath, scope);
        var sayHello = scope.GetVariable<Func<string, string>>("main");
        var result = sayHello(name);

        return Ok(result);
    }
}