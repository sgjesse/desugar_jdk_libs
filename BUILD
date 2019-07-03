alias(
    name = "desugar_jdk_libs",
    actual = "//src/share/classes/java",
    visibility = ["//visibility:public"],
)

genrule(
    name = "maven_release",
    srcs = [":desugar_jdk_libs", "VERSION.txt"],
    outs = ["desugar_jdk_libs.zip"],
    cmd = "./$(locations tools/build_maven_artifact.py)"
        + " --jar $(locations :desugar_jdk_libs)"
        + " --version_file $(locations VERSION.txt) --out $@",
    tools = ["tools/build_maven_artifact.py"],
)