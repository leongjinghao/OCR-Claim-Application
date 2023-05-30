using Microsoft.AspNetCore.Mvc;
using Python.Runtime;

[Route("api/[controller]")]
[ApiController]
public class OCRAppController : ControllerBase
{
    [HttpGet("")]
    public IActionResult Get()
    {
        // initialise Pythonnet engine
        if (!PythonEngine.IsInitialized)
        {
            Runtime.PythonDLL = @"C:\Users\leong\AppData\Local\Programs\Python\Python39\python39.dll";
            PythonEngine.Initialize();
        }

        // Acquire the Python Global Interpreter Lock (GIL)
        using (Py.GIL())
        {
            dynamic sys = Py.Import("sys");
            sys.path.append("Scripts");

            dynamic OCRAppScript = Py.Import("OCRApp");
            var result = OCRAppScript.main();

            return Ok(result.ToString());
        }
    }
}