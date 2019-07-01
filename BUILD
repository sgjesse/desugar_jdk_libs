alias(
    name = "desugar_jdk_libs",
    actual = "//src/share/classes/java",
    visibility = ["//visibility:public"],
)

genrule(
    name = "maven",
    srcs = [":desugar_jdk_libs"],
    outs = ["maven.zip"],
    cmd = "./$(locations tools/build_maven_artifact.py) --jar $(locations :desugar_jdk_libs) --out $@",
    tools = ["tools/build_maven_artifact.py"],
)