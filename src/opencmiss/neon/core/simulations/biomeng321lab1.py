'''
   Copyright 2015 University of Auckland

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
import os
import numpy
from tempfile import NamedTemporaryFile

from opencmiss.iron import iron
from opencmiss.neon.core.simulations.local import LocalSimulation


class Biomeng321Lab1(LocalSimulation):

    def __init__(self):
        super(Biomeng321Lab1, self).__init__()
        self.setName('Biomeng321 Lab1 Simulation')

        self._out_exnode_file = None
        self._out_exelem_file = None

    def getNodeFilename(self):
        return self._out_exnode_file

    def getElementFilename(self):
        return self._out_exelem_file

    def validate(self):
        return True

    def setup(self):
        out_file_handle = NamedTemporaryFile(prefix='biomeng321_lab1_', suffix='.exnode', delete=False)
        self._out_exnode_file = out_file_handle.name
        out_file_handle.close()

        out_file_handle = NamedTemporaryFile(prefix='biomeng321_lab1_', suffix='.exelem', delete=False)
        self._out_exelem_file = out_file_handle.name
        out_file_handle.close()

    def execute(self):
        # Set constants
        X, Y, Z = (1, 2, 3)

        # Set problem parameters
        width = 1.0
        length = 1.0
        height = 1.0
        model = self._parameters['boundary_condition']
        UsePressureBasis = False
        NumberOfGaussXi = 2

        coordinateSystemUserNumber = 1
        regionUserNumber = 1
        basisUserNumber = 1
        pressureBasisUserNumber = 2
        generatedMeshUserNumber = 1
        meshUserNumber = 1
        decompositionUserNumber = 1
        geometricFieldUserNumber = 1
        fibreFieldUserNumber = 2
        materialFieldUserNumber = 3
        dependentFieldUserNumber = 4
        strainFieldUserNumber = 5
        equationsSetFieldUserNumber = 6
        deformedFieldUserNumber = 7
        pressureFieldUserNumber = 8
        equationsSetUserNumber = 1
        problemUserNumber = 1

        # Set all diganostic levels on for testing
        # iron.DiagnosticsSetOn(iron.DiagnosticTypes.ALL,[1,2,3,4,5],"diagnostics.txt",[])

        numberOfLoadIncrements = 1
        numberGlobalXElements = 1
        numberGlobalYElements = 1
        numberGlobalZElements = 1
        InterpolationType = 1
        numberOfXi = 3

        # Get the number of computational nodes and this computational node number
        numberOfComputationalNodes = iron.ComputationalNumberOfNodesGet()
#         computationalNodeNumber = iron.ComputationalNodeNumberGet()

        # Create a 3D rectangular cartesian coordinate system
        coordinateSystem = iron.CoordinateSystem()

        coordinateSystem.CreateStart(coordinateSystemUserNumber)
        coordinateSystem.DimensionSet(3)
        coordinateSystem.CreateFinish()

        # Create a region and assign the coordinate system to the region
        region = iron.Region()
        region.CreateStart(regionUserNumber, iron.WorldRegion)
        region.LabelSet("Region")
        region.coordinateSystem = coordinateSystem
        region.CreateFinish()

        # Define basis
        basis = iron.Basis()
        basis.CreateStart(basisUserNumber)
        if InterpolationType in (1, 2, 3, 4):
            basis.type = iron.BasisTypes.LAGRANGE_HERMITE_TP
        elif InterpolationType in (7, 8, 9):
            basis.type = iron.BasisTypes.SIMPLEX
        basis.numberOfXi = numberOfXi
        basis.interpolationXi = (
            [iron.BasisInterpolationSpecifications.LINEAR_LAGRANGE] * numberOfXi)
        if(NumberOfGaussXi > 0):
            basis.quadratureNumberOfGaussXi = [NumberOfGaussXi] * numberOfXi
        basis.CreateFinish()

        if(UsePressureBasis):
            # Define pressure basis
            pressureBasis = iron.Basis()
            pressureBasis.CreateStart(pressureBasisUserNumber)
            if InterpolationType in (1, 2, 3, 4):
                pressureBasis.type = iron.BasisTypes.LAGRANGE_HERMITE_TP
            elif InterpolationType in (7, 8, 9):
                pressureBasis.type = iron.BasisTypes.SIMPLEX
            pressureBasis.numberOfXi = numberOfXi
            pressureBasis.interpolationXi = (
                [iron.BasisInterpolationSpecifications.LINEAR_LAGRANGE] * numberOfXi)
            if(NumberOfGaussXi > 0):
                pressureBasis.quadratureNumberOfGaussXi = [NumberOfGaussXi] * numberOfXi
            pressureBasis.CreateFinish()

        # Start the creation of a generated mesh in the region
        generatedMesh = iron.GeneratedMesh()
        generatedMesh.CreateStart(generatedMeshUserNumber, region)
        generatedMesh.type = iron.GeneratedMeshTypes.REGULAR
        if(UsePressureBasis):
            generatedMesh.basis = [basis, pressureBasis]
        else:
            generatedMesh.basis = [basis]
            generatedMesh.extent = [width, length, height]
            generatedMesh.numberOfElements = (
                [numberGlobalXElements, numberGlobalYElements, numberGlobalZElements])
        # Finish the creation of a generated mesh in the region
        mesh = iron.Mesh()
        generatedMesh.CreateFinish(meshUserNumber, mesh)

        # Create a decomposition for the mesh
        decomposition = iron.Decomposition()
        decomposition.CreateStart(decompositionUserNumber, mesh)
        decomposition.type = iron.DecompositionTypes.CALCULATED
        decomposition.numberOfDomains = numberOfComputationalNodes
        decomposition.CreateFinish()

        # Create a field for the geometry
        geometricField = iron.Field()
        geometricField.CreateStart(geometricFieldUserNumber, region)
        geometricField.MeshDecompositionSet(decomposition)
        geometricField.TypeSet(iron.FieldTypes.GEOMETRIC)
        geometricField.VariableLabelSet(iron.FieldVariableTypes.U, "Geometry")
        geometricField.ComponentMeshComponentSet(iron.FieldVariableTypes.U, 1, 1)
        geometricField.ComponentMeshComponentSet(iron.FieldVariableTypes.U, 2, 1)
        geometricField.ComponentMeshComponentSet(iron.FieldVariableTypes.U, 3, 1)
        if InterpolationType == 4:
            geometricField.fieldScalingType = iron.FieldScalingTypes.ARITHMETIC_MEAN
        geometricField.CreateFinish()

        # Update the geometric field parameters from generated mesh
        generatedMesh.GeometricParametersCalculate(geometricField)

        # Create a fibre field and attach it to the geometric field
        fibreField = iron.Field()
        fibreField.CreateStart(fibreFieldUserNumber, region)
        fibreField.TypeSet(iron.FieldTypes.FIBRE)
        fibreField.MeshDecompositionSet(decomposition)
        fibreField.GeometricFieldSet(geometricField)
        fibreField.VariableLabelSet(iron.FieldVariableTypes.U, "Fibre")
        if InterpolationType == 4:
            fibreField.fieldScalingType = iron.FieldScalingTypes.ARITHMETIC_MEAN
        fibreField.CreateFinish()

        # Create a deformed geometry field, as cmgui doesn't like displaying
        # deformed fibres from the dependent field because it isn't a geometric field.
        deformedField = iron.Field()
        deformedField.CreateStart(deformedFieldUserNumber, region)
        deformedField.MeshDecompositionSet(decomposition)
        deformedField.TypeSet(iron.FieldTypes.GEOMETRIC)
        deformedField.VariableLabelSet(iron.FieldVariableTypes.U, "DeformedGeometry")
        for component in [1, 2, 3]:
            deformedField.ComponentMeshComponentSet(
                    iron.FieldVariableTypes.U, component, 1)
        if InterpolationType == 4:
            deformedField.ScalingTypeSet(iron.FieldScalingTypes.ARITHMETIC_MEAN)
        deformedField.CreateFinish()

        pressureField = iron.Field()
        pressureField.CreateStart(pressureFieldUserNumber, region)
        pressureField.MeshDecompositionSet(decomposition)
        pressureField.VariableLabelSet(iron.FieldVariableTypes.U, "Pressure")
        pressureField.ComponentMeshComponentSet(
                iron.FieldVariableTypes.U, 1, 1)
        pressureField.ComponentInterpolationSet(iron.FieldVariableTypes.U, 1, iron.FieldInterpolationTypes.ELEMENT_BASED)
        pressureField.NumberOfComponentsSet(iron.FieldVariableTypes.U, 1)
#         if InterpolationType == 4:
#             pressureField.ScalingTypeSet(iron.FieldScalingTypes.GEOMETRIC_MEAN)
        pressureField.CreateFinish()

        # Create the equations_set
        equationsSetField = iron.Field()
        equationsSet = iron.EquationsSet()

        problemSpecification = [iron.ProblemClasses.ELASTICITY,
            iron.ProblemTypes.FINITE_ELASTICITY,
            iron.EquationsSetSubtypes.MOONEY_RIVLIN]
        equationsSet.CreateStart(equationsSetUserNumber, region, fibreField, problemSpecification,
            equationsSetFieldUserNumber, equationsSetField)
        equationsSet.CreateFinish()

        # Create the dependent field
        dependentField = iron.Field()
        equationsSet.DependentCreateStart(dependentFieldUserNumber, dependentField)
        dependentField.VariableLabelSet(iron.FieldVariableTypes.U, "Dependent")
        dependentField.ComponentInterpolationSet(iron.FieldVariableTypes.U, 4, iron.FieldInterpolationTypes.ELEMENT_BASED)
        dependentField.ComponentInterpolationSet(iron.FieldVariableTypes.DELUDELN, 4, iron.FieldInterpolationTypes.ELEMENT_BASED)
        if(UsePressureBasis):
            # Set the pressure to be nodally based and use the second mesh component
            if InterpolationType == 4:
                dependentField.ComponentInterpolationSet(iron.FieldVariableTypes.U, 4, iron.FieldInterpolationTypes.NODE_BASED)
                dependentField.ComponentInterpolationSet(iron.FieldVariableTypes.DELUDELN, 4, iron.FieldInterpolationTypes.NODE_BASED)
            dependentField.ComponentMeshComponentSet(iron.FieldVariableTypes.U, 4, 2)
            dependentField.ComponentMeshComponentSet(iron.FieldVariableTypes.DELUDELN, 4, 2)
        if InterpolationType == 4:
            dependentField.fieldScalingType = iron.FieldScalingTypes.ARITHMETIC_MEAN
        equationsSet.DependentCreateFinish()

        # Initialise dependent field from undeformed geometry and displacement bcs and set hydrostatic pressure
        iron.Field.ParametersToFieldParametersComponentCopy(
            geometricField, iron.FieldVariableTypes.U, iron.FieldParameterSetTypes.VALUES, 1,
            dependentField, iron.FieldVariableTypes.U, iron.FieldParameterSetTypes.VALUES, 1)
        iron.Field.ParametersToFieldParametersComponentCopy(
            geometricField, iron.FieldVariableTypes.U, iron.FieldParameterSetTypes.VALUES, 2,
            dependentField, iron.FieldVariableTypes.U, iron.FieldParameterSetTypes.VALUES, 2)
        iron.Field.ParametersToFieldParametersComponentCopy(
            geometricField, iron.FieldVariableTypes.U, iron.FieldParameterSetTypes.VALUES, 3,
            dependentField, iron.FieldVariableTypes.U, iron.FieldParameterSetTypes.VALUES, 3)
        iron.Field.ComponentValuesInitialiseDP(
            dependentField, iron.FieldVariableTypes.U, iron.FieldParameterSetTypes.VALUES, 4, 0.0)

        # Create the material field
        materialField = iron.Field()
        equationsSet.MaterialsCreateStart(materialFieldUserNumber, materialField)
        materialField.VariableLabelSet(iron.FieldVariableTypes.U, "Material")
        equationsSet.MaterialsCreateFinish()

        # Set Mooney-Rivlin constants c10 and c01 respectively.
        materialField.ComponentValuesInitialiseDP(
            iron.FieldVariableTypes.U, iron.FieldParameterSetTypes.VALUES, 1, 1.0)
        materialField.ComponentValuesInitialiseDP(
            iron.FieldVariableTypes.U, iron.FieldParameterSetTypes.VALUES, 2, 0.2)

        # Create a Guass point based field for calculated strain
        strainField = iron.Field()
        strainField.CreateStart(strainFieldUserNumber, region)
        strainField.MeshDecompositionSet(decomposition)
        strainField.TypeSet(iron.FieldTypes.GENERAL)
        strainField.GeometricFieldSet(geometricField)
        strainField.DependentTypeSet(iron.FieldDependentTypes.DEPENDENT)
        strainField.VariableTypesSet([iron.FieldVariableTypes.U])
        strainField.VariableLabelSet(iron.FieldVariableTypes.U, "Strain")
        strainField.NumberOfComponentsSet(iron.FieldVariableTypes.U, 6)
        for component in range(1, 7):
            strainField.ComponentInterpolationSet(
                    iron.FieldVariableTypes.U, component,
                    iron.FieldInterpolationTypes.GAUSS_POINT_BASED)
        strainField.CreateFinish()

        equationsSet.DerivedCreateStart(strainFieldUserNumber, strainField)
        equationsSet.DerivedVariableSet(iron.EquationsSetDerivedTypes.STRAIN,
                iron.FieldVariableTypes.U)
        equationsSet.DerivedCreateFinish()

        # Create equations
        equations = iron.Equations()
        equationsSet.EquationsCreateStart(equations)
        equations.sparsityType = iron.EquationsSparsityTypes.SPARSE
        equations.outputType = iron.EquationsOutputTypes.NONE
        equationsSet.EquationsCreateFinish()

        # Define the problem
        problem = iron.Problem()
        problemSpecification = [iron.ProblemClasses.ELASTICITY,
                iron.ProblemTypes.FINITE_ELASTICITY,
                iron.ProblemSubtypes.NONE]
        problem.CreateStart(problemUserNumber, problemSpecification)
        problem.CreateFinish()

        # Create the problem control loop
        problem.ControlLoopCreateStart()
        controlLoop = iron.ControlLoop()
        problem.ControlLoopGet([iron.ControlLoopIdentifiers.NODE], controlLoop)
        controlLoop.MaximumIterationsSet(numberOfLoadIncrements)
        problem.ControlLoopCreateFinish()

        # Create problem solver
        nonLinearSolver = iron.Solver()
        linearSolver = iron.Solver()
        problem.SolversCreateStart()
        problem.SolverGet([iron.ControlLoopIdentifiers.NODE], 1, nonLinearSolver)
        nonLinearSolver.outputType = iron.SolverOutputTypes.PROGRESS
        nonLinearSolver.NewtonJacobianCalculationTypeSet(
                iron.JacobianCalculationTypes.EQUATIONS)
        nonLinearSolver.NewtonLinearSolverGet(linearSolver)
        linearSolver.linearType = iron.LinearSolverTypes.DIRECT
        # linearSolver.libraryType = iron.SolverLibraries.LAPACK
        problem.SolversCreateFinish()

        # Create solver equations and add equations set to solver equations
        solver = iron.Solver()
        solverEquations = iron.SolverEquations()
        problem.SolverEquationsCreateStart()
        problem.SolverGet([iron.ControlLoopIdentifiers.NODE], 1, solver)
        solver.SolverEquationsGet(solverEquations)
        solverEquations.sparsityType = iron.SolverEquationsSparsityTypes.SPARSE
        _ = solverEquations.EquationsSetAdd(equationsSet)
        problem.SolverEquationsCreateFinish()

        # Prescribe boundary conditions (absolute nodal parameters)
        boundaryConditions = iron.BoundaryConditions()
        solverEquations.BoundaryConditionsCreateStart(boundaryConditions)
        if model == 1:
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 1, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 3, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 5, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 7, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 2, X, iron.BoundaryConditionsTypes.FIXED, 0.5)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 4, X, iron.BoundaryConditionsTypes.FIXED, 0.5)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 6, X, iron.BoundaryConditionsTypes.FIXED, 0.5)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 8, X, iron.BoundaryConditionsTypes.FIXED, 0.5)

            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 1, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 2, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 5, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 6, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)

            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 1, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 2, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 3, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 4, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)

        elif model == 2:
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 1, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 3, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 5, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 7, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 2, X, iron.BoundaryConditionsTypes.FIXED, 0.25)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 4, X, iron.BoundaryConditionsTypes.FIXED, 0.25)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 6, X, iron.BoundaryConditionsTypes.FIXED, 0.25)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 8, X, iron.BoundaryConditionsTypes.FIXED, 0.25)

            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 1, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 2, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 5, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 6, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 3, Y, iron.BoundaryConditionsTypes.FIXED, 0.25)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 4, Y, iron.BoundaryConditionsTypes.FIXED, 0.25)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 7, Y, iron.BoundaryConditionsTypes.FIXED, 0.25)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 8, Y, iron.BoundaryConditionsTypes.FIXED, 0.25)

            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 1, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 2, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 3, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 4, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)

        elif model == 3:
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 1, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 3, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 5, X, iron.BoundaryConditionsTypes.FIXED, 0.5)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 7, X, iron.BoundaryConditionsTypes.FIXED, 0.5)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 2, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 4, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 6, X, iron.BoundaryConditionsTypes.FIXED, 0.5)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 8, X, iron.BoundaryConditionsTypes.FIXED, 0.5)

            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 1, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 2, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 5, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 6, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)

            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 1, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 2, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 3, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 4, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 5, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 6, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 7, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 8, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)

        elif model == 4:
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 1, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 3, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 6, X, iron.BoundaryConditionsTypes.FIXED, 0.5)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 8, X, iron.BoundaryConditionsTypes.FIXED, 0.5)

            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 1, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 2, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 5, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 6, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)

            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 1, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 3, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 6, Z, iron.BoundaryConditionsTypes.FIXED, 0.5)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 8, Z, iron.BoundaryConditionsTypes.FIXED, 0.5)

        elif model == 5:
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 1, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 3, X, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 5, X, iron.BoundaryConditionsTypes.FIXED, 0.5)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 7, X, iron.BoundaryConditionsTypes.FIXED, 0.5)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 2, X, iron.BoundaryConditionsTypes.FIXED, 0.25)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 4, X, iron.BoundaryConditionsTypes.FIXED, 0.25)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 6, X, iron.BoundaryConditionsTypes.FIXED, 0.75)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 8, X, iron.BoundaryConditionsTypes.FIXED, 0.75)

            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 1, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 2, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 5, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 6, Y, iron.BoundaryConditionsTypes.FIXED, 0.0)

            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 1, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 2, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 3, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 4, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 5, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 6, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 7, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)
            boundaryConditions.AddNode(dependentField, iron.FieldVariableTypes.U, 1, 1, 8, Z, iron.BoundaryConditionsTypes.FIXED, 0.0)

        solverEquations.BoundaryConditionsCreateFinish()

        # Solve the problem
        problem.Solve()

        # Copy deformed geometry into deformed field
        for component in [1, 2, 3]:
            dependentField.ParametersToFieldParametersComponentCopy(
                iron.FieldVariableTypes.U,
                iron.FieldParameterSetTypes.VALUES, component,
                deformedField, iron.FieldVariableTypes.U,
                iron.FieldParameterSetTypes.VALUES, component)

        # Copy pressure into pressure field
        dependentField.ParametersToFieldParametersComponentCopy(
                iron.FieldVariableTypes.U,
                iron.FieldParameterSetTypes.VALUES, 4,
                pressureField, iron.FieldVariableTypes.U,
                iron.FieldParameterSetTypes.VALUES, 1)

        # Export results
        fields = iron.Fields()
        fields.CreateRegion(region)
        fields.NodesExport(self._out_exnode_file, "FORTRAN")
        fields.ElementsExport(self._out_exelem_file, "FORTRAN")
        fields.Finalise()

        results = {}
        elementNumber = 1
        xiPosition = [0.5, 0.5, 0.5]
        F = equationsSet.TensorInterpolateXi(
            iron.EquationsSetTensorEvaluateTypes.DEFORMATION_GRADIENT,
            elementNumber, xiPosition, (3, 3))
        results['Deformation Gradient Tensor'] = F

        C = equationsSet.TensorInterpolateXi(
            iron.EquationsSetTensorEvaluateTypes.R_CAUCHY_GREEN_DEFORMATION,
            elementNumber, xiPosition, (3, 3))
        results['Right Cauchy-Green Deformation Tensor'] = C

        E = equationsSet.TensorInterpolateXi(
            iron.EquationsSetTensorEvaluateTypes.GREEN_LAGRANGE_STRAIN,
            elementNumber, xiPosition, (3, 3))
        results['Green-Lagrange Strain Tensor'] = E

        I1 = numpy.trace(C)
        I2 = 0.5 * (numpy.trace(C) ** 2. - numpy.tensordot(C, C))
        I3 = numpy.linalg.det(C)
        results['Invariants'] = [I1, I2, I3]
#         print("Invariants")
#         print("I1={0}, I2={1}, I3={2}".format(I1, I2, I3))

        TC = equationsSet.TensorInterpolateXi(
            iron.EquationsSetTensorEvaluateTypes.CAUCHY_STRESS,
            elementNumber, xiPosition, (3, 3))
        results['Cauchy Stress Tensor'] = TC

        # Output of Second Piola-Kirchhoff Stress Tensor not implemented. It is
        # instead, calculated from TG=J*F^(-1)*TC*F^(-T), where T indicates the
        # transpose fo the matrix.
        # TG = equationsSet.TensorInterpolateXi(
        #    iron.EquationsSetTensorEvaluateTypes.SECOND_PK_STRESS,
        #    elementNumber, xiPosition,(3,3))
#         J = 1.  # Assumes J=1
        TG = numpy.dot(numpy.linalg.inv(F), numpy.dot(
                TC, numpy.linalg.inv(numpy.matrix.transpose(F))))
        results['Second Piola-Kirchhoff Stress Tensor'] = TG

        # Note that the hydrostatic pressure value is different from the value quoted
        # in the original lab instructions. This is because the stress has been
        # evaluated using modified invariants
        p = dependentField.ParameterSetGetElement(
            iron.FieldVariableTypes.U,
            iron.FieldParameterSetTypes.VALUES, elementNumber, 4)
        results['Hydrostatic pressure'] = p

        return results

    def cleanup(self):
        os.rename(self._out_exnode_file + '.part0.exnode', self._out_exnode_file)
        os.rename(self._out_exelem_file + '.part0.exelem', self._out_exelem_file)
