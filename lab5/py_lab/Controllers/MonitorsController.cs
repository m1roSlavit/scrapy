using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using py_lab.Models;
using Microsoft.AspNetCore.Authorization;

namespace py_lab.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class MonitorsController : ControllerBase
    {

        private readonly FPYTHONLAB5PY_LABMYDBMDFContext _context;

        public MonitorsController(FPYTHONLAB5PY_LABMYDBMDFContext context)
        {
            _context = context;
        }

        //[HttpGet]
        //public async Task<ActionResult<IEnumerable<Monitor>>> GetMonitors()
        //{
        //    return await _context.Monitor.ToListAsync();
        //}

        [HttpGet]
        public async Task<ActionResult<Monitor>> GetMonitors([FromQuery(Name = "model")] string model)
        {
            var monitor = await _context.Monitor.FirstOrDefaultAsync(e => e.Model == model);

            if (monitor == null)
            {
                return NotFound();
            }

            return monitor;
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<Monitor>> GetMonitors(int id)
        {
            var monitor = await _context.Monitor.FindAsync(id);

            if (monitor == null)
            {
                return NotFound();
            }

            return monitor;
        }

        [HttpPut]
        public async Task<IActionResult> PutMonitors(Monitor monitor)
        {

            var result = await _context.Monitor.FirstOrDefaultAsync(b => b.Link == monitor.Link);
            if (result != null)
            {
                result.Model = monitor.Model;
                result.Price = monitor.Price;
                await _context.SaveChangesAsync();
            }
            else
            {
                return BadRequest();
            }

            return NoContent();
        }

        [HttpPost]
        public async Task<ActionResult<Monitor>> PostMonitors(Monitor monitor)
        {
            if(_context.Monitor.Any(b => b.Model == monitor.Model && b.Price == monitor.Price && b.Link == monitor.Link))
            {
                return Conflict();
            }
            _context.Monitor.Add(monitor);
            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateException)
            {
                if (MonitorsExists(monitor.Id))
                {
                    return Conflict();
                }
                else
                {
                    throw;
                }
            }
            return CreatedAtAction("GetMonitors", new { id = monitor.Id }, monitor);
        }

        [HttpDelete("{id}")]
        public async Task<ActionResult<Monitor>> DeleteMonitors(int id)
        {
            var monitor = await _context.Monitor.FindAsync(id);
            if (monitor == null)
            {
                return NotFound();
            }

            _context.Monitor.Remove(monitor);
            await _context.SaveChangesAsync();

            return monitor;
        }

        private bool MonitorsExists(int id)
        {
            return _context.Monitor.Any(e => e.Id == id);
        }
    }
}
