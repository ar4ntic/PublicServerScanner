"""
Core functionality for the Public Server Scanner Tool.

This module orchestrates all the security scans and provides the main
run function for both command-line and GUI operation.
"""

import os
import sys
import logging
import threading
from typing import Dict, List, Tuple, Any, Optional, Callable

from app.utils import create_output_dir, setup_logging
from app.config import Config
from app.constants import APP_NAME, APP_VERSION, APP_YEAR, APP_AUTHOR
from app.checks.ping import ping_target
from app.checks.portscan import port_scan
from app.checks.bruteforce import directory_bruteforce
from app.checks.dns import dns_enumeration
from app.checks.cert import certificate_details
from app.checks.headers import gather_headers

# Initialize logger
logger = logging.getLogger(__name__)

def get_available_checks() -> Dict[str, Callable]:
    """
    Get all available security checks.
    
    Returns:
        Dict[str, Callable]: Dictionary mapping check names to functions
    """
    return {
        'ping': ping_target,
        'port_scan': port_scan,
        'bruteforce': directory_bruteforce,
        'dns': dns_enumeration,
        'cert': certificate_details,
        'headers': gather_headers
    }

class TaskRunner:
    """Run scan tasks with progress updates."""
    
    def __init__(self, tasks, target, output_dir, 
                 progress_callback=None, complete_callback=None):
        """
        Initialize the task runner.
        
        Args:
            tasks (List[Callable]): List of check functions to run
            target (str): Target hostname or IP
            output_dir (str): Directory to save scan results
            progress_callback (Callable, optional): Function to call with progress updates
            complete_callback (Callable, optional): Function to call when all tasks complete
        """
        self.tasks = tasks
        self.target = target
        self.output_dir = output_dir
        self.progress_callback = progress_callback
        self.complete_callback = complete_callback
        self.results = []
        self.running = False
        self.thread = None
        
    def start(self):
        """Start running tasks in a separate thread."""
        self.running = True
        self.thread = threading.Thread(target=self._run_tasks)
        self.thread.daemon = True
        self.thread.start()
        
    def _run_tasks(self):
        """Run all tasks and collect results."""
        config = Config()
        parallel = config.get("scan_threads", 1) > 1
        
        for i, task in enumerate(self.tasks):
            if not self.running:
                break
                
            # Update progress
            if self.progress_callback:
                self.progress_callback(i, len(self.tasks), task.__name__)
                
            # Run the task
            success = task(self.target, self.output_dir)
            self.results.append((task.__name__, success))
        
        # Final callback
        if self.complete_callback and self.running:
            self.complete_callback(self.results)
        
        self.running = False
    
    def stop(self):
        """Stop running tasks."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.1)

def run(args):
    """
    Main entry point for the security scan.
    
    Args:
        args (argparse.Namespace): Command line arguments
    
    Returns:
        bool: True if all checks succeeded, False otherwise
    """
    # Set up logging
    logger = setup_logging()
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    
    # Validate target
    if not args.target:
        try:
            # Try to use GUI if available
            import tkinter as tk
            from tkinter import simpledialog
            root = tk.Tk()
            root.withdraw()
            target = simpledialog.askstring("Input", "Enter target hostname or IP:")
            if not target:
                logger.error("No target specified")
                return False
            args.target = target
        except ImportError:
            logger.error("No target specified and tkinter not available for GUI prompt")
            return False
    
    # Create output directory
    output_dir = create_output_dir(args.target)
    logger.info(f"Results will be saved to {output_dir}")
    
    # Determine which checks to run
    available_checks = get_available_checks()
    
    if args.checks:
        # Run specific checks
        checks_to_run = []
        for check_name in args.checks:
            if check_name not in available_checks:
                logger.warning(f"Unknown check: {check_name}")
                continue
            checks_to_run.append(available_checks[check_name])
    else:
        # Run all checks by default
        checks_to_run = list(available_checks.values())
    
    # Run the checks
    if args.gui:
        # Run in GUI mode with progress updates
        try:
            return run_gui_mode(args.target, output_dir, checks_to_run)
        except ImportError:
            logger.warning("GUI mode requested but tkinter not available, falling back to CLI mode")
            return run_cli_mode(args.target, output_dir, checks_to_run)
    else:
        # Run in CLI mode
        return run_cli_mode(args.target, output_dir, checks_to_run)

def run_cli_mode(target, output_dir, checks):
    """
    Run security checks in command-line interface mode.
    
    Args:
        target (str): Target hostname or IP
        output_dir (str): Directory to save results
        checks (List[Callable]): List of check functions to run
    
    Returns:
        bool: True if all checks succeeded, False otherwise
    """
    logger.info(f"Running CLI mode security scan on {target}")
    
    all_success = True
    for i, check in enumerate(checks):
        logger.info(f"Running {check.__name__} ({i+1}/{len(checks)})...")
        success = check(target, str(output_dir))
        if success:
            logger.info(f"{check.__name__} completed successfully")
        else:
            logger.error(f"{check.__name__} failed")
            all_success = False
    
    logger.info(f"Security scan complete. Results saved to {output_dir}")
    return all_success

def run_gui_mode(target, output_dir, checks):
    """
    Run security checks with a GUI progress display.
    
    Args:
        target (str): Target hostname or IP
        output_dir (str): Directory to save results
        checks (List[Callable]): List of check functions to run
    
    Returns:
        bool: True if all checks succeeded, False otherwise
    """
    import tkinter as tk
    from tkinter import ttk, messagebox
    
    logger.info(f"Running GUI mode security scan on {target}")
    
    # Create progress window
    root = tk.Tk()
    root.title("Public Server Scanner Progress")
    root.geometry("600x400")
    
    # Add progress elements
    progress_frame = tk.Frame(root)
    progress_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    tk.Label(progress_frame, text=f"Target: {target}", font=("Helvetica", 12)).grid(
        row=0, column=0, columnspan=2, sticky=tk.W, pady=5
    )
    tk.Label(progress_frame, text=f"Output Directory: {output_dir}", font=("Helvetica", 10)).grid(
        row=1, column=0, columnspan=2, sticky=tk.W, pady=5
    )
    
    progress_label = tk.Label(progress_frame, text="Initializing...")
    progress_label.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)
    
    # Progress bar
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100)
    progress_bar.grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5)
    
    # Status text area with scrollbar
    status_frame = tk.Frame(progress_frame)
    status_frame.grid(row=4, column=0, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S, pady=5)
    progress_frame.rowconfigure(4, weight=1)
    progress_frame.columnconfigure(1, weight=1)
    
    scrollbar = tk.Scrollbar(status_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    status_text = tk.Text(status_frame, height=10, yscrollcommand=scrollbar.set)
    status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=status_text.yview)
    
    # Store results for the complete callback
    scan_results = []
    
    def update_progress(current, total, task_name):
        """Update progress UI."""
        progress_var.set((current + 1) / total * 100)
        progress_label.config(text=f"Running {task_name}... ({current + 1}/{total})")
        status_text.insert(tk.END, f"Starting {task_name}...\n")
        status_text.see(tk.END)
        root.update_idletasks()
        
    def scan_completed(task_results):
        """Handle scan completion."""
        status_text.insert(tk.END, "\n=== Scan Completed ===\n")
        
        # Report on successes and failures
        failures = [name for name, success in task_results if not success]
        if failures:
            status_text.insert(tk.END, f"\nThe following scans failed: {', '.join(failures)}\n")
            status_text.insert(tk.END, "Check the log file for details.\n")
        
        status_text.insert(tk.END, f"\nResults saved in: {output_dir}\n")
        status_text.see(tk.END)
        
        # Update UI
        progress_label.config(text="Scan completed")
        
        # Show completion message
        messagebox.showinfo("Scan Complete", f"Security scan completed!\nResults saved in: {output_dir}")
        root.destroy()
        
        # Store the results in the enclosing scope
        nonlocal scan_results
        scan_results = task_results
    
    # Start the task runner
    runner = TaskRunner(
        tasks=checks,
        target=target,
        output_dir=str(output_dir),
        progress_callback=update_progress,
        complete_callback=scan_completed
    )
    
    # Add a cancel button
    button_frame = tk.Frame(progress_frame)
    button_frame.grid(row=5, column=0, columnspan=2, sticky=tk.E, pady=5)
    
    cancel_button = tk.Button(
        button_frame, 
        text="Cancel", 
        command=lambda: [runner.stop(), root.destroy()]
    )
    cancel_button.pack(side=tk.RIGHT, padx=5)
    
    # Start running tasks
    runner.start()
    
    # Start the GUI event loop
    root.mainloop()
    
    # Check if all tasks succeeded
    all_success = all(success for _, success in scan_results)
    return all_success