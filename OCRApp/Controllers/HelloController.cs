using Microsoft.AspNetCore.Mvc;
using Python.Runtime;

[Route("api/[controller]")]
[ApiController]
public class HelloController : ControllerBase
{
    [HttpGet("{name}")]
    public IActionResult Get(string name)
    {
        // var engine = Python.CreateEngine();
        // var scope = engine.CreateScope();

        // string pythonScriptPath = Path.Combine(Directory.GetCurrentDirectory(), "Scripts", "HelloScript.py");

        // engine.ExecuteFile(pythonScriptPath, scope);
        // var sayHello = scope.GetVariable<Func<string, string>>("main");
        // var result = sayHello(name);

        // return Ok(result);

        if (!PythonEngine.IsInitialized)
        {
            Runtime.PythonDLL = @"C:\Users\leong\AppData\Local\Programs\Python\Python39\python39.dll";
            PythonEngine.Initialize();
        }

        using (Py.GIL()) // Acquire the Python Global Interpreter Lock (GIL)
        {
            dynamic sys = Py.Import("sys");
            sys.path.append("Scripts");

            dynamic helloScript = Py.Import("HelloScript");
            string result = helloScript.sayhello(name);

            return Ok(result);
        }
    }
}