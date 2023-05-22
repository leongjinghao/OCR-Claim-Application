using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using IronPython.Hosting;

[Route("api/[controller]")]
[ApiController]
public class OCRAppController : ControllerBase
{
    [HttpGet("")]
    public IActionResult Get()
    {
        var engine = Python.CreateEngine();
        var scope = engine.CreateScope();
        
        string OCRAppScriptPath = Path.Combine(Directory.GetCurrentDirectory(), "Scripts", "OCRApp.py");

        engine.ExecuteFile(OCRAppScriptPath, scope);
        var OCRApp = scope.GetVariable<Func<IronPython.Runtime.PythonTuple>>("main");
        var result = OCRApp();

        return Ok(result);
    }
}