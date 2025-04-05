from mcp.server.fastmcp import FastMCP
import os
import logging
from typing import Dict, Any, Optional, Union
from gromacs_copilot.core.md_agent import MDLLMAgent 


# Initialize FastMCP server
mcp = FastMCP("gromacs-copilot")

# Reference to the agent instance (will be set later)
global agent

@mcp.tool()
async def init_gromacs_copilot(workspace: str, gmx_bin: str) -> Dict[str, Any]:
    """
    Initialize the GROMACS Copilot server with a specific workspace and GROMACS binary
    
    Args:
        workspace: Path to the workspace directory
        gmx_bin: Path to the GROMACS binary
        **kwargs: Additional arguments for agent initialization
    """
    global agent
    agent = MDLLMAgent(workspace=workspace, api_key="dummy", gmx_bin=gmx_bin)
    
    return {"success": True, "message": f"Initialized GROMACS Copilot with workspace: {workspace}"}


@mcp.tool()
async def check_gromacs_installation() -> Dict[str, Any]:
    """
    Check if GROMACS is installed and available
    
    Returns:
        Dictionary with GROMACS installation information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    
    return agent.protocol.check_gromacs_installation()

@mcp.tool()
async def set_protein_file(file_path: str) -> Dict[str, Any]:
    """
    Set and prepare the protein file for simulation, only use for protein-ligand complex
    
    Args:
        file_path: Path to the protein structure file (PDB or GRO)
        
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    elif hasattr(agent.protocol, "set_protein_file"):
        
        return agent.protocol.set_protein_file(file_path)
    else:
        return {"success": False, "error": "set_protein_file method not available in agent, is not needed for protein only simulation."}

@mcp.tool()
async def check_for_ligands(pdb_file: str) -> Dict[str, Any]:
    """
    Check for potential ligands in the PDB file, only use for protein-ligand complex
    
    Args:
        pdb_file: Path to the PDB file
        
    Returns:
        Dictionary with ligand information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    
    return agent.protocol.check_for_ligands(pdb_file)

@mcp.tool()
async def set_ligand(ligand_name: str) -> Dict[str, Any]:
    """
    Set the ligand for simulation, only use for protein-ligand complex
    
    Args:
        ligand_name: Residue name of the ligand in the PDB file
        
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    
    return agent.protocol.set_ligand(ligand_name)

@mcp.tool()
async def generate_topology(force_field: str, water_model: str = "spc") -> Dict[str, Any]:
    """
    Generate topology for the protein
    
    Args:
        force_field: Name of the force field to use
        water_model: Water model to use
        
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    return agent.protocol.generate_topology(force_field, water_model)

@mcp.tool()
async def define_simulation_box(distance: float = 1.0, box_type: str = "cubic") -> Dict[str, Any]:
    """
    Define the simulation box
    
    Args:
        distance: Minimum distance between protein and box edge (nm)
        box_type: Type of box (cubic, dodecahedron, octahedron)
        
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}

    return agent.protocol.define_simulation_box(distance, box_type)

@mcp.tool()
async def solvate_system() -> Dict[str, Any]:
    """
    Solvate the protein in water
    
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    return agent.protocol.solvate_system()

@mcp.tool()
async def create_mdp_file(mdp_type: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create an MDP parameter file for GROMACS
    
    Args:
        mdp_type: Type of MDP file
        params: Optional override parameters
        
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}

    return agent.protocol.create_mdp_file(mdp_type, params)

@mcp.tool()
async def add_ions(concentration: float = 0.15, neutral: bool = True) -> Dict[str, Any]:
    """
    Add ions to the solvated system
    
    Args:
        concentration: Salt concentration in M
        neutral: Whether to neutralize the system
        
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}

    return agent.protocol.add_ions(concentration, neutral)

@mcp.tool()
async def run_energy_minimization() -> Dict[str, Any]:
    """
    Run energy minimization
    
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    # global agent
    return agent.protocol.run_energy_minimization()

@mcp.tool()
async def run_nvt_equilibration() -> Dict[str, Any]:
    """
    Run NVT equilibration
    
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    # global agent
    return agent.protocol.run_nvt_equilibration()

@mcp.tool()
async def run_npt_equilibration() -> Dict[str, Any]:
    """
    Run NPT equilibration
    
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    # global agent
    return agent.protocol.run_npt_equilibration()

@mcp.tool()
async def run_production_md(length_ns: float = 10.0) -> Dict[str, Any]:
    """
    Run production MD
    
    Args:
        length_ns: Length of the simulation in nanoseconds
        
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    # global agent
    return agent.protocol.run_production_md(length_ns)

@mcp.tool()
async def analyze_rmsd() -> Dict[str, Any]:
    """
    Perform RMSD analysis
    
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    # global agent
    return agent.protocol.analyze_rmsd()

@mcp.tool()
async def analyze_rmsf() -> Dict[str, Any]:
    """
    Perform RMSF analysis
    
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    # global agent
    return agent.protocol.analyze_rmsf()

@mcp.tool()
async def analyze_gyration() -> Dict[str, Any]:
    """
    Perform radius of gyration analysis
    
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    # global agent
    return agent.protocol.analyze_gyration()

@mcp.tool()
async def analyze_ligand_rmsd() -> Dict[str, Any]:
    """
    Perform RMSD analysis focused on the ligand
    
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    # global agent
    return agent.protocol.analyze_ligand_rmsd()

@mcp.tool()
async def analyze_protein_ligand_contacts() -> Dict[str, Any]:
    """
    Analyze contacts between protein and ligand
    
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    # global agent
    return agent.protocol.analyze_protein_ligand_contacts()

@mcp.tool()
async def set_simulation_stage(stage: str) -> Dict[str, Any]:
    """
    Set the current simulation stage
    
    Args:
        stage: Name of the stage to set
        
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    # global agent
    return agent.protocol.set_simulation_stage(stage)

@mcp.tool()
async def run_shell_command(command: str, capture_output: bool = True) -> Dict[str, Any]:
    """
    Run a shell command
    
    Args:
        command: Shell command to run
        capture_output: Whether to capture stdout/stderr
        
    Returns:
        Dictionary with command result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    # global agent
    return agent.protocol.run_shell_command(command, capture_output)

@mcp.tool()
async def get_workspace_info() -> Dict[str, Any]:
    """
    Get information about the current workspace
    
    Returns:
        Dictionary with workspace information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    # global agent
    return agent.protocol.get_state()

# Add additional tools for MM-PBSA functionality
@mcp.tool()
async def switch_agent_protocol(protocol:str) -> Dict[str, Any]:
    """
    Switch to another protocol
    Args:
        protocol: Name of the protocol to switch to, [ligand, mmpbsa, analysis]
    
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    if protocol not in ["ligand", "mmpbsa, analysis"]:
        return {"success": False, "error": "protocol not supported"}
    elif protocol == "mmpbsa":
        agent.switch_to_mmpbsa_protocol()
        return {"success": True, "message": "switched to mmpbsa protocol"}
    elif protocol == "ligand":
        agent.switch_to_protein_ligand_protocol()
        return {"success": True, "message": "switched to ligand protocol"}
    elif protocol == "analysis":
        agent.switch_to_analysis_protocol()
        return {"success": True, "message": "switched to analysis protocol"}
    


@mcp.tool()
async def create_mmpbsa_index_file(protein_selection: str = "Protein", 
                                 ligand_selection: str = "LIG") -> Dict[str, Any]:
    """
    Create index file for MM-PBSA analysis
    
    Args:
        protein_selection: Selection for protein group
        ligand_selection: Selection for ligand group
        
    Returns:
        Dictionary with result information
    """
    global agent
    if agent is None:
        return {"success": False, "error": "agent not initialized"}
    # global agent
    return agent.protocol.create_mmpbsa_index_file(protein_selection, ligand_selection)

