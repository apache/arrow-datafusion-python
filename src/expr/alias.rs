// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

use crate::expr::PyExpr;
use pyo3::prelude::*;
use std::fmt::{self, Display, Formatter};

use datafusion_expr::Expr;

#[pyclass(name = "Alias", module = "datafusion.expr", subclass)]
#[derive(Clone)]
pub struct PyAlias {
    expr: PyExpr,
    alias_name: String,
}

impl Display for PyAlias {
    fn fmt(&self, f: &mut Formatter) -> fmt::Result {
        write!(
            f,
            "Alias
            \nExpr: `{:?}`
            \nAlias Name: `{}`",
            &self.expr, &self.alias_name
        )
    }
}

impl PyAlias {
    pub fn new(expr: &Box<Expr>, alias_name: &String) -> Self {
        let py_expr = *(*expr).clone();
        Self {
            expr: py_expr.into(),
            alias_name: alias_name.clone(),
        }
    }
}

#[pymethods]
impl PyAlias {
    /// Retrieve the "name" of the alias
    fn alias(&self) -> PyResult<String> {
        Ok(self.alias_name.clone())
    }

    fn expr(&self) -> PyResult<PyExpr> {
        Ok(self.expr.clone())
    }

    /// Get a String representation of this column
    fn __repr__(&self) -> String {
        format!("{}", self)
    }
}
