using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata;

// Code scaffolded by EF Core assumes nullable reference types (NRTs) are not used or disabled.
// If you have enabled NRTs for your project, then un-comment the following line:
// #nullable disable

namespace py_lab.Models
{
    public partial class FPYTHONLAB5PY_LABMYDBMDFContext : DbContext
    {
        public FPYTHONLAB5PY_LABMYDBMDFContext()
        {
        }

        public FPYTHONLAB5PY_LABMYDBMDFContext(DbContextOptions<FPYTHONLAB5PY_LABMYDBMDFContext> options)
            : base(options)
        {
        }

        public virtual DbSet<Monitor> Monitor { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                optionsBuilder.UseSqlServer("Data Source=(LocalDB)\\MSSQLLocalDB;AttachDbFilename=F:\\python\\lab5\\py_lab\\MyDB.mdf;Integrated Security=True");
            }
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Monitor>(entity =>
            {
                entity.Property(e => e.Link)
                    .HasColumnName("link")
                    .HasMaxLength(50);

                entity.Property(e => e.Model)
                    .HasColumnName("model")
                    .HasMaxLength(50);

                entity.Property(e => e.Price).HasColumnName("price");
            });

            OnModelCreatingPartial(modelBuilder);
        }

        partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
    }
}
