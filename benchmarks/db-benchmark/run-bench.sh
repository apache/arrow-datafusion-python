#!/bin/bash
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
set -e

#SRC_DATANAME=G1_1e7_1e2_0_0 python3 /db-benchmark/polars/groupby-polars.py
SRC_DATANAME=G1_1e7_1e2_0_0 python3 /db-benchmark/datafusion-python/groupby-datafusion.py

# joins need more work still
#SRC_DATANAME=G1_1e7_1e2_0_0 python3 /db-benchmark/datafusion-python/join-datafusion.py
#SRC_DATANAME=G1_1e7_1e2_0_0 python3 /db-benchmark/polars/join-polars.py

cat time.csv
